from django.conf.urls import url

from .views import account_register
from .views import account_register_success
from .views import account_register_confirm

urlpatterns = [
    url(r'^register/$', account_register, name='account-register'),
    url(r'^register/success/$', account_register_success, name='account-register-success'),
    url(r'^register/confirm/(?P<user_id>\d+)/(?P<uuid>[\w-]+)/$', account_register_confirm, name='account-register-confirm'),
]
