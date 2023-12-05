from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('index', views.start, name='index'),
    path('home', views.home, name='home'),
    path('initiative/edit/<record>', views.edit_item, name='edit_item'),
    path('initiative/delete/<record>', views.delete_item, name='delete_item'),
    path('save_org', views.save_org, name='save_org'),
    path('save_project/<int:org_id>', views.save_project, name='save_project'),
    path('save_choice/<type>/<name>', views.save_choice, name='save_choice'),
    path('populate_db', views.populate_db),
    path('populate_db_initiatives', views.populate_db_initiatives),
    path('assessment_review', views.assessment_review, name='assessment_review'),
    path('review_score', views.review_score, name='review_score'),
    path('calculate_score', views.calculate_score, name='calculate_score'),
    path('<pk>/initiative', views.initiative, name='initiative'),
    path('<pk>/submit_initiatives', views.submit_initiatives, name='submit_initiatives'),
    path('add_initiative', views.add_initiative, name='add_initiative'),
    path('create_link/<test_taker_id>', views.create_link, name='create_link'),
    path('', views.LogInView.as_view(), name='log_in'),
    path('log-out/', views.LogOutView.as_view(), name='logout'),
    path('user_home/<id>/<token>', views.user_home, name='user_home'),
    path('user_home/<id>/start_survey/<token>', views.start_survey, name='start_survey'),
    path('finish_test', views.finish_test, name='finish_test'),
    path('categorical_questions/<category>/<id>/<token>', views.categorical_questions, name='categorical_questions'),
    path('get_questions/<category>/<id>/<token>', views.get_questions, name='get_questions'),
    path('help&faq', views.help_faq, name='help_faq'),

    path('api/get-project-choices/<int:org_id>/', views.get_project_choices, name='get_project_choices'),
    path('api/get-orgs/', views.get_orgs, name='get_orgs'),
    path('api/get-projs/', views.get_projs, name='get_projs'),

    path('resend/activation-code/', views.ResendActivationCodeView.as_view(), name='resend_activation_code'),
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', views.ActivateView.as_view(), name='activate'),
    path('restore/password/', views.RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', views.RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', views.RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),
    path('remind/username/', views.RemindUsernameView.as_view(), name='remind_username'),
    path('change/profile/', views.ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', views.ChangeEmailView.as_view(), name='change_email'),
    path('change/email/<code>/', views.ChangeEmailActivateView.as_view(), name='change_email_activation'),
    path('admin_login', views.AdminLogin.as_view(), name='admin_login'),
    path('radar-chart/', views.radar_chart, name='radar_chart'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
