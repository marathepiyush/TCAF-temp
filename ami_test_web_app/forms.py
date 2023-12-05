from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import UserInfo, Org, Project, InitiativeDetail


class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))

        return password


class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('Username'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return username


class EmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email


class SignInViaEmailForm(SignIn, EmailForm):
    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']


class EmailOrUsernameForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('Email or Username'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address or username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email_or_username


class SignInViaEmailOrUsernameForm(SignIn, EmailOrUsernameForm):
    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email_or_username', 'password', 'remember_me']
        return ['email_or_username', 'password']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=_('Email'), help_text=_('Required. Enter an existing email address.'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(_('You can not use this email address.'))

        return email


class ResendActivationCodeForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('Email or Username'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address or username.'))

        if user.is_active:
            raise ValidationError(_('This account has already been activated.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Activation code not found.'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Activation code has already been sent. You can request a new code in 24 hours.'))

        self.user_cache = user

        return email_or_username


class ResendActivationCodeViaEmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if user.is_active:
            raise ValidationError(_('This account has already been activated.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Activation code not found.'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Activation code has already been sent. You can request a new code in 24 hours.'))

        self.user_cache = user

        return email


class RestorePasswordForm(EmailForm):
    pass


class RestorePasswordViaEmailOrUsernameForm(EmailOrUsernameForm):
    pass


class ChangeProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=30, required=False)
    last_name = forms.CharField(label=_('Last name'), max_length=150, required=False)


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == self.user.email:
            raise ValidationError(_('Please enter another email.'))

        user = User.objects.filter(Q(email__iexact=email) & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('You can not use this mail.'))

        return email


class RemindUsernameForm(EmailForm):
    pass


class UserInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].choices = self.get_project_choices()

    class Meta:
        model = UserInfo
        # fields = '__all__'
        exclude = ['password_change_required']

    org = forms.ModelChoiceField(queryset=Org.objects.all(), label= "Organization")
    project = forms.ChoiceField(choices=(), required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="Set Password")
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput, label="Confirm Password")

    def get_project_choices(self):
        org_id = self.data.get('org')
        if org_id:
            c = [(sub.project, sub.project) for sub in Project.objects.filter(org=Org.objects.get(id=org_id))]
            return c
        return []

class OrgForm(forms.ModelForm):
    poc_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter the name of point of Contact'}))
    poc_email = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter the email of point of Contact'}))
    poc_role = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter the current role of point of Contact in the organization'}))
    class Meta:
        model = Org
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrgForm, self).__init__(*args, **kwargs)
        self.fields['org'].label = 'Organization'
        self.fields['poc_name'].label = 'Name'
        self.fields['poc_email'].label = 'Email'
        self.fields['poc_role'].label = 'Role'


class ProjectForm(forms.ModelForm):
    org = forms.CharField(widget=forms.HiddenInput)
    project = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter the name of Project here'}))
    duration = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Please enter in months'}), max_value=12)
    class Meta:
        model = Project
        fields = '__all__'


class InitiativeForm(forms.ModelForm):

    class Meta:
        model = InitiativeDetail
        fields = '__all__' #['initiative', 'description', 'tieback']

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(required=True, widget=forms.PasswordInput, label="One Time Password")
    new_password = forms.CharField(required=True, widget=forms.PasswordInput, label="New Password")