from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth import views

from .models import Account
from .forms import UserCreateForm
from .forms import LoginForm

def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):

    form = LoginForm()
    context = {'form': form}

    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('login-success'))
        else:
            context['fail'] = True

    return render(request, 'authentication/login.html', context)

def login_success(request):
    return render(request, 'authentication/login-success.html')

def login_failed(request):
    return render(request, 'authentication/login-failed.html')

def account_register_confirm(request, user_id, uuid):
    context = {}
    try:
        acc = Account.objects.get(pk=user_id, key=uuid)
        if acc.is_active:
            context['msg'] = 'already_activated'
        else:
            acc.is_active = True
            acc.save()
            context['msg'] = 'success'

    except Account.DoesNotExist:
        context['msg'] = 'failed'

    return render(request, 'authentication/register-confirm.html', context)

def account_register(request):
    if request.method == 'POST':

        form = UserCreateForm(request.POST)

        if form.is_valid():

            user = form.save()

            confirm_link = "{}{}".format(request.META['HTTP_HOST'], reverse('account-register-confirm', args=(user.id,user.key,)))
            text_template = get_template('authentication/email_register.txt')
            html_template = get_template('authentication/email_register.html')
            text_content = text_template.render(Context({'confirm_link': confirm_link}))
            html_content = html_template.render(Context({'confirm_link': confirm_link}))

            subject = 'E-mail verification'
            to = [user.email]

            msg = EmailMultiAlternatives(subject, text_content, to=to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return HttpResponseRedirect(reverse('account-register-success'))
    else:
        form = UserCreateForm()

    return render(request, 'authentication/register.html', {'form': form})

def account_register_success(request):
    return render(request, 'authentication/register-success.html')

def account_forgot(request):

    context = {}

    if request.method == 'POST':

        email = request.POST.get('email', '')

        try:
            account = Account.objects.get(email=email)
            if account.is_active == True:

                # Generate new user key and reset its expiration time
                key = account.set_new_key()
                keytime = account.reset_keytime()

                reset_link = "{}{}".format(request.META['HTTP_HOST'], reverse('account-forgot-reset', args=(account.id,account.key,)))
                text_template = get_template('authentication/email_password_reset.txt')
                html_template = get_template('authentication/email_password_reset.html')
                text_content = text_template.render(Context({'user': account, 'reset_link': reset_link}))
                html_content = html_template.render(Context({'user': account, 'reset_link': reset_link}))

                subject = 'Password reset'
                to = [account.email]

                msg = EmailMultiAlternatives(subject, text_content, to=to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            else:
                context['not_active'] = True

        except Account.DoesNotExist:
            pass

    return render(request, 'authentication/forgot.html', context)

def account_forgot_reset(request, user_id, uuid):
    context = {}

    try:
        if request.method == 'POST':

            key = request.POST.get('key','')
            user_id = request.POST.get('user_id','')
            new_password = request.POST.get('new_password', '')

            account = Account.objects.get(is_active=True, id=user_id, key=key)

            if new_password >= 8:
                account.set_password(new_password)
                account.key = None
                account.keytime = None
                account.save()
            else:
                context['msg'] = 'Password too short'
        else:
            account = Account.objects.get(is_active=True, id=user_id, key=uuid)
            context['account'] = account

    except ValueError:
        pass

    except Account.DoesNotExist:
        pass

    return render(request, 'authentication/forgot_reset.html', context)
