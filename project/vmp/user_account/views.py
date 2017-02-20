from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib import auth

from malwaredb.forms import UserCreationForm
from malwaredb.views import malware_signup, malware_upload
from user_account.models import UserAccount

from datetime import datetime


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print form
        if form.is_valid():
            print "testing."
            user = form.save()
            user_account = UserAccount.objects.create(user=user, create_date=datetime.now())

            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None and user.is_active:
                auth.login(request, user)
        else:
            return malware_upload(request, state="signup_fail")

    return malware_upload(request, state="signup_success")
        # return render(request, 'malware_signup.html',
        #               {'signup_success': True}, )


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None and user.is_active:
                auth.login(request, user)
        else:
            return malware_upload(request, state="login_fail")
            # return HttpResponseRedirect('/malwareupload/?login_fail=True')

    return malware_upload(request, state="login_success")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')
