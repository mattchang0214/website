from accounts.forms import EmailValidation
from django.conf.urls import url
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_reset/$', password_reset,
        {
            'template_name': 'accounts/password_reset/password_reset_form.html',
            'password_reset_form': EmailValidation,
            'html_email_template_name': 'accounts/password_reset/password_reset_email.html',
            'email_template_name': 'accounts/password_reset/password_reset_email.html',
            'subject_template_name': 'accounts/password_reset/password_reset_subject.txt',
            'post_reset_redirect': 'accounts:password_reset_done'
        },
        name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done,
        {
            'template_name': 'accounts/password_reset/password_reset_done.html'
        },
        name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {
            'template_name': 'accounts/password_reset/password_reset_confirm.html',
            'post_reset_redirect': 'accounts:password_reset_complete'
        },
        name='password_reset_confirm'),
    url(r'^password_reset/complete/$', password_reset_complete,
        {
            'template_name': 'accounts/password_reset/password_reset_complete.html'
        },
        name='password_reset_complete'),
]
