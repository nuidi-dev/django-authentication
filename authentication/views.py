from django.shortcuts import render
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from authentication.forms import UserCreateForm

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from .models import Account

def account_register_confirm(request, user_id, uuid):

    try:
        acc = Account.objects.get(pk=user_id, activation_key=uuid)
        if acc.is_active:
            return render(request, 'authentication/register-confirm.html', {'msg': 'already_activated'})

        acc.is_active = True
        acc.save()
        return render(request, 'authentication/register-confirm.html', {'msg': 'success'})

    except Account.DoesNotExist:
        return render(request, 'authentication/register-confirm.html', {'msg': 'failed'})

def account_register(request):
    if request.method == 'POST':

        form = UserCreateForm(request.POST)

        if form.is_valid():

            user = form.save()

            confirm_link = "{}{}".format(request.META['HTTP_HOST'], reverse('account-register-confirm', args=(user.id,user.activation_key,)))
            text_template = get_template('authentication/confirm-email.txt')
            html_template = get_template('authentication/confirm-email.html')
            text_content = text_template.render(Context({'confirm_link': confirm_link}))
            html_content = html_template.render(Context({'confirm_link': confirm_link}))

            subject = 'E-mail verification'
            from_email = 'nuxitpl@gmail.com'
            to_email = [user.email]

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return HttpResponseRedirect(reverse('account-register-success'))
    else:
        form = UserCreateForm()

    return render(request, 'authentication/register.html', {'form': form})

def account_register_success(request):
    return render(request, 'authentication/register-success.html')
