from django.conf.urls import url

from .views import account_register
from .views import account_register_success
from .views import account_register_confirm
from .views import login_view
from .views import login_success
from .views import logout_view

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^login/success/$', login_success, name='login-success'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', account_register, name='account-register'),
    url(r'^register/success/$', account_register_success, name='account-register-success'),
    url(r'^register/confirm/(?P<user_id>\d+)/(?P<uuid>[\w-]+)/$', account_register_confirm, name='account-register-confirm'),
]
