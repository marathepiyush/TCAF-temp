import ast
import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import View, FormView, TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _
from .forms import (
    SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
    RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
    ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeProfileForm, ChangeEmailForm,
    UserInfoForm, OrgForm, ProjectForm, InitiativeForm, PasswordChangeForm
)
from .utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
    create_token, send_email, is_superuser_or_staff
)
from .tables import QuestionsTable
from ast import literal_eval
from django_tables2 import RequestConfig
import boto3
import html
import base64
from datetime import datetime, timedelta
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


@login_required()
@user_passes_test(is_superuser_or_staff)
def initiative(request, pk):
    if request.method == 'POST':
        if 'Submit' in request.POST:
            return redirect('submit_initiatives', pk=pk)
        try:
            obj = FinalInitiatives.objects.get(user_id=UserInfo.objects.get(pk=pk))
            temp = []
            temp.extend(ast.literal_eval(obj.data))
            temp.extend(request.POST.getlist('selection'))
            obj.data = temp
            obj.save()
        except FinalInitiatives.DoesNotExist:
            obj = FinalInitiatives()
            obj.user_id = UserInfo.objects.get(pk=pk)
            obj.data = request.POST.getlist('selection')
            obj.save()
        return redirect('initiative', pk=pk)
    category = request.GET.get('category')
    if category:
        obj = InitiativeDetail.objects.filter(category=Categories.objects.get(name=category))
        table = QuestionsTable(obj)
        table.paginate(page=request.GET.get("page", 1), per_page=5)
        RequestConfig(request).configure(table)
        table_html = table.as_html(request)
        return HttpResponse(table_html)
    else:
        obj = InitiativeDetail.objects.all()
    table = QuestionsTable(obj)
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    categories_obj = literal_eval(literal_eval(UserCategories.objects.get(user_id=pk).response))
    dimension = {}
    del categories_obj['csrfmiddlewaretoken']
    for i in categories_obj:
        dimension[i.split('_')[0]] = []
    for i in categories_obj:
        if len(i.split('_')) == 2:
            dimension[i.split('_')[0]].append(i.split('_')[1])
    return render(request, 'Initiative.html', {'table': table,
                                               'form': InitiativeForm(),
                                               'pk': pk,
                                               'user': request.user,
                                               'dimension': dimension,
                                               'first_dimension': next(iter(dimension))})

@login_required()
@user_passes_test(is_superuser_or_staff)
def submit_initiatives(request, pk):

    obj = FinalInitiatives.objects.get(user_id=UserInfo.objects.get(pk=pk))
    data = ast.literal_eval(obj.data)
    dimensions = {}
    for i in data:
        initiativedetail_obj = InitiativeDetail.objects.get(pk=int(i))
        dimensions[initiativedetail_obj.dimension] = []
    for i in data:
        initiativedetail_obj = InitiativeDetail.objects.get(pk=int(i))
        dimensions[initiativedetail_obj.dimension].append(initiativedetail_obj)
    return render(request, 'suggestion.html', {'dimensions': dimensions})

@login_required()
@user_passes_test(is_superuser_or_staff)
def add_initiative(request):
    form = InitiativeForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('initiative', pk=request.session.get('test_taker_id'))


@login_required()
@user_passes_test(is_superuser_or_staff)
def edit_item(request, record):
    item = InitiativeDetail.objects.get(initiative_id=record)
    if request.method == 'POST':
        form = InitiativeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('initiative', request.session.get('test_taker_id'))
    else:
        form = InitiativeForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})


@login_required()
@user_passes_test(is_superuser_or_staff)
def delete_item(request, record):
    item = InitiativeDetail.objects.get(initiative_id=record)
    if request.method == 'POST':
        item.delete()
        return redirect('initiative', pk=request.session.get('test_taker_id'))
    return render(request, 'delete_item.html', {'item': item, 'pk': request.session.get('test_taker_id')})


@login_required()
@user_passes_test(is_superuser_or_staff)
def home(request):
    return render(request, 'home_page_admin.html', {'user': request.user})

@login_required()
@user_passes_test(is_superuser_or_staff)
def start(request):
    form = UserInfoForm()
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = UserInfo.objects.filter(email__iexact=email).exists()
            # if user:
            #     raise ValidationError(_('You can not use this email address.'))
            test_taker = form.save(commit=True)
            user = User()
            user.username = f"{test_taker.fullname.split()[0]}{test_taker.id}"
            user.set_password(test_taker.password)
            user.save()
            return redirect('create_link', test_taker.id)
    return render(request, 'Register1.html', {'form': form,
                                              'user': request.user})


@login_required()
@user_passes_test(is_superuser_or_staff)
def create_link(request, test_taker_id):
    test_taker = UserInfo.objects.get(id=test_taker_id)
    obj = UserCategories()
    obj.user_id = test_taker
    obj.response = json.dumps(ProjectOrgChoices.objects.get(name=test_taker.project).response)
    host = request.META['HTTP_HOST']
    token = create_token()
    obj.token = token
    obj.save()
    link = f'{host}/user_home/{test_taker.id}/{token}'
    subject = 'Hello. This is a test email from TCAF'
    firstname = test_taker.fullname.split()[0]
    body = f'''
                <h1>Hey <u>{firstname}</u>! Please find the link below for taking assessment </h1>
                <h3>{link}</h3>
                <h3>ID: {test_taker.id}</h3>
                <h3>Username: {firstname}{test_taker.id}</h3>
                <h3>Password: <b>{test_taker.password}</b></h3>
    '''
    email = EmailMultiAlternatives(subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=[test_taker.email])
    email.attach_alternative(body, "text/html")
    email.send()
    admin = request.user.username
    context = {
        'test_taker': test_taker,
        'admin': admin,
        'link': link,
        'username': f'{firstname}{test_taker.id}'
    }
    return render(request, 'survey_detail.html', context)


@login_required
def start_survey(request, id, token):
    question_info = request.session['user_categories_list']
    dimension = {}
    for i in question_info:
        if '_' in i:
            dimension.setdefault(i.split('_')[0], []).append(i.split('_')[1])
    first_category = ''
    for i in question_info:
        if len(i.split('_'))>1:
            first_category = i.split('_')[1]
            break
    context = {
        'dimension': dimension,
        'id': id,
        'token': token,
        'first_dimension': next(iter(dimension)),
        'first_category': first_category
    }
    return render(request, 'Assessment_Page.html', context)



def save_response(id, token, user_data):
    obj = UserResponse.objects.filter(user_id__exact=id)
    if obj.exists():
        obj = obj[0]
        data = literal_eval(obj.response)
        for key in user_data:
            if not data.get(key):
                data[key] = user_data[key]
            elif data[key] != user_data[key]:
                data[key] = user_data[key]
        obj.response = json.dumps(data)
        obj.save()
    else:
        response = UserResponse()
        response.user_id = UserInfo.objects.get(id=id)
        response.token = token
        response.response = json.dumps(user_data)
        response.save()


def finish_test(request):
    return render(request, 'save_response.html')


@login_required()
def get_questions(request, category, id, token):
    if '__' in category:
        category = category.replace('__', '/')
    if request.method == 'POST':
        if 'finish_test' in request.POST:
            return render(request, 'save_response.html')
        data = dict(request.POST) # Converting QueryDict to Dict
        del data['csrfmiddlewaretoken']
        for i in list(data.keys()):
            if data[i] == ['']:
                del data[i]
        # Saving file to media folder in this loop
        for i in request.FILES:
            uploaded_file = request.FILES[i]
            data[i] = uploaded_file.name
            request.session['uploaded_file'] = base64.b64encode(uploaded_file.read()).decode('utf-8')
            upload_path = os.path.join(settings.BASE_DIR, 'media', id, token)
            # Create the upload_path folder if it does not exist
            os.makedirs(upload_path, exist_ok=True)
            with open(os.path.join(upload_path, uploaded_file.name), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Saving the upload info in a table, so it can be fetched later
            obj = UploadedFile()
            obj.user_id = UserInfo.objects.get(pk=id)
            obj.token = token
            obj.question_id = Questions.objects.get(pk=i)
            obj.file = uploaded_file
            obj.save()
        # Save the POST data to UserResponse table
        save_response(id=id, token=token, user_data={category: data})
        response = HttpResponse(f'''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"><h2>Responses submitted for {category}. Please click 
        the next category to proceed.</h2><br><br><a href="{reverse('finish_test')}" target="_parent">
        <button type="button" class="btn btn-success btn-lg">Finish Assessment</button></a>''')
        expires_date = datetime.now() + timedelta(days=10) # expire cookie after 10 days
        if request.COOKIES.get('answered_questions'):
            response.set_cookie('answered_questions', literal_eval(request.COOKIES.get('answered_questions'))|data, max_age=300)
        else:
            response.set_cookie('answered_questions', data, max_age=300)
        return response
    category = html.unescape(category)
    questions = Questions.objects.filter(category=Categories.objects.get(name=category))
    context = {'questions': questions}
    return render(request, 'questions.html', context)


@login_required
def categorical_questions(request, category, id, token):
    user_categories_list = [i.split('_')[-1] for i in request.session['user_categories_list'] if '_' in i]
    if request.session['category_index'] == len(user_categories_list) - 1:
        form_data = dict(request.POST)
        del form_data['csrfmiddlewaretoken']
        request.session['user_response'][category] = form_data
        user_data = request.session["user_response"]
        return redirect('save_response', id, token, user_data)
    if category == 'None':
        category = user_categories_list[0]
    else:
        request.session['category_index'] += 1
        category = user_categories_list[request.session['category_index']]
        form_data = dict(request.POST)
        del form_data['csrfmiddlewaretoken']
    if request.session['category_index'] > 0:
        prev_category = user_categories_list[request.session['category_index'] - 1]
        request.session['user_response'][prev_category] = form_data
    questions = Questions.objects.filter(category=Categories.objects.get(name=category))
    question_info = request.session['user_categories_list']
    dimension = {}
    for i in question_info:
        if '_' in i:
            dimension.setdefault(i.split('_')[0], []).append(i.split('_')[1])
    if category == user_categories_list[-1]:
        return render(request, 'business_alignment.html', {
            'category': category,
            'questions': questions,
            'category_dict': dimension,
            'id': id,
            'token': token,
            'finished': True
        })
    context = {
        'category': category,
        'questions': questions,
        'category_dict': dimension,
        'id': id,
        'token': token
    }
    return render(request, 'business_alignment.html', context)


@login_required()
@user_passes_test(is_superuser_or_staff)
def get_project_choices(request, org_id):
    choices = list(Project.objects.filter(org_id=org_id).values('id', 'project'))
    return JsonResponse({'choices': choices})


@login_required()
@user_passes_test(is_superuser_or_staff)
def get_orgs(request):
    orgs = Org.objects.all()
    return JsonResponse({'orgs': [i.org for i in orgs]})


@login_required()
@user_passes_test(is_superuser_or_staff)
def get_projs(request):
    org = Org.objects.get(id=request.GET['org'])
    projects = Project.objects.filter(org=org)
    return JsonResponse({'projects': [i.project for i in projects]})


@login_required()
@user_passes_test(is_superuser_or_staff)
def save_choice(request, type, name):
    if type == 'Org':
        Org_main = Org.objects.filter(org__iexact=name)
        project_org = ProjectOrgChoices.objects.filter(name__iexact=name)
        if Org_main.exists():
            if project_org.exists():
                obj = project_org[0]
                obj.response = dict(request.POST)
                obj.save()
                return redirect('save_org')
            choice_obj = ProjectOrgChoices()
            choice_obj.type = type
            choice_obj.name = name
            choice_obj.response = dict(request.POST)
            choice_obj.save()
        else:
            resp = 'The Organisation does not exist. Please save Organisation and then customize assessment'
            return HttpResponse(resp)
        return redirect('save_org')
    else:
        Proj_main = Project.objects.filter(project__iexact=name)
        project_org = ProjectOrgChoices.objects.filter(name__iexact=name, type__iexact='Project')
        if Proj_main.exists():
            if project_org.exists():
                obj = project_org[0]
                obj.response = dict(request.POST)
                obj.save()
                return redirect('index')
            choice_obj = ProjectOrgChoices()
            choice_obj.type = type
            choice_obj.name = name
            choice_obj.response = dict(request.POST)
            choice_obj.save()
        else:
            resp = 'The Organisation does not exist. Please save Organisation and then customize assessment'
            return HttpResponse(resp)
        return redirect('index')


@login_required()
@user_passes_test(is_superuser_or_staff)
def save_org(request):
    form = OrgForm()
    if request.method == 'POST':
        form = OrgForm(request.POST)
        org = Org.objects.filter(org__iexact=request.POST['org'])
        org_exists = org.exists()
        request.session['skip'] = False
        if "poc_role" in request.POST:
            request.session['skip'] = True
        if not org_exists and form.is_valid():
            form.save()
        if 'save_choices' in request.POST:
            customization_form = {}
            dimensions = Dimensions.objects.all()
            for dimension in dimensions:
                customization_form[dimension] = []
            for dimension in customization_form:
                categories = Categories.objects.filter(dimension=dimension)
                for category in categories:
                    customization_form[dimension].append(category)
            choices = []
            if ProjectOrgChoices.objects.filter(name__iexact=request.POST['org']).exists():
                Org_choices = literal_eval(ProjectOrgChoices.objects.get(name=request.POST['org']).response)
                choices = Org_choices.keys()
            context = {
                'type': 'Org',
                'save_choice': request.POST['org'],
                'test_taker': request.user,
                'choices': choices,
                'customization_form': customization_form
            }
            return render(request, 'customize_assessment_1.html', context)
        return redirect('save_project', org_id=org[0].id)
    return render(request, 'save_org.html', {'form': form})


@login_required()
@user_passes_test(is_superuser_or_staff)
def save_project(request, org_id):
    form = ProjectForm()
    org = Org.objects.get(id=org_id)
    skip = request.session.get('skip')
    if request.method == 'POST':
        req_copy = request.POST.copy()
        req_copy[org] = org.org
        proj = Project.objects.filter(project__iexact=request.POST['project'])
        proj_exists = proj.exists()
        if not proj_exists:
            proj_obj = Project()
            proj_obj.project = request.POST['project']
            proj_obj.duration = request.POST['duration']
            proj_obj.leader = request.POST['leader']
            proj_obj.description = request.POST['description']
            proj_obj.org = org
            proj_obj.save()

        if 'save_choices' in request.POST:
            customization_form = {}
            dimensions = Dimensions.objects.all()
            for dimension in dimensions:
                customization_form[dimension] = []
            for dimension in customization_form:
                categories = Categories.objects.filter(dimension=dimension)
                for category in categories:
                    customization_form[dimension].append(category)
            try:
                Org_choices = literal_eval(ProjectOrgChoices.objects.get(name=org.org).response)
            except:
                Org_choices = {}
            context = {
                'type': 'Project',
                'save_choice': request.POST['project'],
                'test_taker': request.user,
                'choices': list(Org_choices.keys()),
                'customization_form': customization_form
            }
            return render(request, 'customize_assessment_1.html', context)
    return render(request, 'save_project.html', {'form': form, 'org': org, 'skip': skip})


@login_required
def user_home(request, id, token):
    user_categories = UserCategories.objects.get(user_id=id)
    user_obj = UserInfo.objects.get(pk=id)

    if user_categories.token != token:
        logout(request)
        return redirect('log_in')

    form = PasswordChangeForm()
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('current_password') != user_obj.password:
                return render(request, 'password_change.html', {'form': form,
                                                                'incorrect_current_password': True})
            user_obj.password = form.cleaned_data.get('new_password')
            user_obj.confirm_password = form.cleaned_data.get('new_password')
            user_obj.password_change_required = False
            user_obj.save()
            username = user_obj.fullname.split()[0]+str(user_obj.pk)
            user = User.objects.get(username=username)
            user.set_password(user_obj.password)
            user.save()
            login(request, user)
            request.session['user_categories_list'] = literal_eval(literal_eval(user_categories.response))
            request.session['category_index'] = 0
            request.session['user_response'] = {}
            context = {'id': id, 'token': token}
            return render(request, 'user_home.html', context)

    if user_obj.password_change_required:
        return render(request, 'password_change.html', {'form': form})

    request.session['user_categories_list'] = literal_eval(literal_eval(user_categories.response))
    request.session['category_index'] = 0
    request.session['user_response'] = {}
    context = {'id': id, 'token': token}
    return render(request, 'user_home.html', context)


@login_required()
@user_passes_test(is_superuser_or_staff)
def assessment_review(request):
    return render(request, 'assessment_review_page.html')


@login_required()
@user_passes_test(is_superuser_or_staff)
def review_score(request):
    form_data = dict(request.POST)
    user_info = UserInfo.objects.get(id=request.POST["user_id"])
    request.session['test_taker_id'] = request.POST.get('user_id')
    user_response_obj = UserResponse.objects.get(user_id=user_info.id)
    user_response = json.loads(user_response_obj.response)
    data = {}
    for categories in user_response:
        data[categories] = {}
        for key, value in user_response[categories].items():
            question_obj = Questions.objects.get(id=key)
            if type(value) is list:
                answer = ','.join(value)
            else:
                answer = value
            data[categories][question_obj] = answer
    return render(request, 'Review&Score.html', {'data': data,
                                                 'id': user_response_obj.user_id.pk,
                                                 'token': user_response_obj.token})


@login_required()
@user_passes_test(is_superuser_or_staff)
def calculate_score(request):
    myDict = dict(request.POST)
    actual_dict = {}
    parsed_category = {}
    all_params = {}
    for i in myDict.keys():
        if "text" in i or "score" in i:
            q_no = i.split("_")[1]
            question = Questions.objects.get(id=str(q_no))
            actual_dict[question] = myDict[i]
        if len(i.split('_')) > 1:
            q_no = i.split("_")[1]
            question = Questions.objects.get(id=str(q_no))
            question_category = question.category
            if question_category not in parsed_category:
                parsed_category[question_category] = 1
                question_dimension = question.dimension
                all_params[question_category.name] = Questions.objects.filter(category=question_category,
                                                                              dimension=question_dimension)
                all_params[question_category.name] = list(set(i.parameter for i in all_params[question_category.name]))

    final_list = []

    for question in actual_dict.keys():
        existing_dimension = False
        dimension_index = 0
        for each_dimension_index, each_dimension in enumerate(final_list):
            if str(question.dimension) in each_dimension.keys():
                existing_dimension = True
                dimension_index = each_dimension_index
                break
        if existing_dimension:
            existing_category = False
            category_index = 0
            for each_category_index, each_category in enumerate(final_list[dimension_index][str(question.dimension)]):
                if str(question.category) in each_category:
                    existing_category = True
                    category_index = each_category_index
                    break
            if existing_category:
                existing_parameter = False
                parameter_index = 0
                for each_parameter_index, each_parameter in enumerate(
                        final_list[dimension_index][str(question.dimension)][category_index][str(question.category)]):
                    if str(question.parameter) in each_parameter:
                        existing_parameter = True
                        parameter_index = each_parameter_index
                        break
                if existing_parameter:
                    average_mark = 0
                    if actual_dict[question] != 'nan':
                        average_mark = (float(list(actual_dict[question])[0]))
                    final_list[dimension_index][str(question.dimension)][category_index][str(question.category)][
                        parameter_index][str(question.parameter)].append(average_mark)
                else:
                    average_mark = 0
                    if actual_dict[question] != 'nan':
                        average_mark = (float(list(actual_dict[question])[0]))
                    final_list[dimension_index][str(question.dimension)][category_index][str(question.category)].append(
                        {question.parameter: [average_mark]})
            else:
                average_mark = 0
                if actual_dict[question] != 'nan':
                    average_mark = (float(list(actual_dict[question])[0]))
                final_list[dimension_index][str(question.dimension)].append(
                    {str(question.category): [{str(question.parameter): [average_mark]}]})
        else:
            average_mark = 0
            if str(actual_dict[question]) != 'nan':
                average_mark = (float(actual_dict[question][0]))
            final_list.append({str(question.dimension): [
                {str(question.category): [{str(question.parameter): [average_mark]}]}]})

    for each_dimension_index, each_dimension in enumerate(final_list):
        for dimension in each_dimension:
            for category_index, category in enumerate(final_list[each_dimension_index][dimension]):
                for parameter in category.keys():
                    avg_calc = 0
                    for each_sub_type in category[parameter]:
                        avg = 0
                        for each in each_sub_type.values():
                            avg = sum(each) / len(all_params[parameter])
                        avg_calc = avg_calc + avg
                    final_list[each_dimension_index][dimension][category_index][parameter] = round(
                        (avg_calc / len(category[parameter])), 1)

    labels = []
    data = []
    for each_category in final_list:
        for value in each_category.values():
            for each in value:
                for each_value in each:
                    labels.append(each_value)
                    data.append(each[each_value])
    context_elements = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'score_summary.html', {'data': final_list,
                                                  'context': context_elements,
                                                  'user_id': request.session.get('test_taker_id')})


def help_faq(request):
    pass

import pandas as pd

excel = r'C:\Users\tumata\Downloads\TCAF Initiatives.xlsx'


def populate_db(request):
    data_df = pd.read_excel(excel, sheet_name='Quality Engineering')
    dict = {
        'dimension': {
            'Category': []
        }
    }

    parameters = data_df['Parameter']
    question = data_df['Question']
    enablement_dependency = data_df['Dependency for Enablement']
    weightage = data_df['Weightage']
    ans_type = data_df['Answer Type']
    options = data_df['Recommended Answer Options']
    dimensions = data_df['Dimension']
    categories = data_df['Category']

    for dimension in dimensions.unique():
        dim = Dimensions()
        dim.name = dimension.strip()
        dim.save()

    for category in categories.unique():
        cat = Categories()
        cat.name = category.strip()
        cat.dimension = Dimensions.objects.get(name='Quality Engineering')
        cat.save()

    for i in range(len(dimensions)):
        question_data = Questions()
        question_data.dimension = Dimensions.objects.get(name=dimensions.iloc[i].strip())
        question_data.category = Categories.objects.get(name=categories.iloc[i].strip())
        question_data.parameter = parameters.iloc[i].strip()
        question_data.question = question.iloc[i].strip()
        question_data.enablement_dependency = enablement_dependency.iloc[i]
        question_data.weightage = weightage.iloc[i]
        question_data.ans_type = ans_type.iloc[i].strip()
        question_data.options = options.iloc[i]
        question_data.save()

    return HttpResponse("<html><body>DB data %s.</body></html>" % dict)


def populate_db_initiatives(request):
    data_df = pd.read_excel(excel, sheet_name='TDM')
    trace = InitiativeTraceability.objects.all()
    # for i in data_df.iloc:
    #     obj = InitiativeTraceability()
    #     obj.dimension = Dimensions.objects.get(name=i['Dimension'])
    #     obj.category = Categories.objects.get(name=i['Category'])
    #     obj.initiatives = i['Initiatives']
    #     obj.save()
    for i in data_df.iloc:
        obj = InitiativeDetail()
        obj.initiative_id = i['ID']
        obj.initiative = i['Initiatives']
        obj.description = i['Description']
        obj.tieback = i['Tie-back To Current State Findings']
        for j in trace:
            if i['ID'] in [x.strip() for x in j.initiatives.split(',')]:
                obj.dimension = j.dimension
                obj.category = j.category
        obj.save()
    return HttpResponse('done')



class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())
        if url_is_safe:
            return redirect(redirect_to)

        return redirect("home")


class SignUpView(GuestOnlyView, FormView):
    template_name = 'sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            # Set a temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = True

        # Create a user record
        user.save()

        # Change the username to the "user_ID" form
        if settings.DISABLE_USERNAME:
            user.username = f'user_{user.id}'
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('You are successfully signed up!'))

        return redirect('index')


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('log_in')


class ResendActivationCodeView(GuestOnlyView, FormView):
    template_name = 'resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('resend_activation_code')


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('restore_password_done')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('change_profile')


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('change_email')


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('remind_username')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'restore_password_confirm.html'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'restore_password_done.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'log_out.html'


class IndexPageView(TemplateView):
    template_name = 'index_v2.html'


class AdminLogin(TemplateView):
    template_name = 'admin_login.html'


def radar_chart(request):
    # replace this with your actual data from DB
    labels = ['Python', 'JavaScript', 'HTML', 'CSS', 'Django']
    data = [90, 80, 85, 70, 91]

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'radar_chart.html', context)
