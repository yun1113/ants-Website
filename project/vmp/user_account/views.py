from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib import auth

from malwaredb.forms import MalwareUploadFileForm, ContactForm, UserCreationForm
from malwaredb.models import Malware, Upload
from user_account.models import UserAccount

from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_account = UserAccount.objects.create(user=user, create_date=datetime.now())

        form = MalwareUploadFileForm()
        malware_num = len(Malware.objects.filter(~Q(detectionrate=0)))
        upload_num = len(Upload.objects.all())
        analysis_num = len(Malware.objects.all())
        signup_form = UserCreationForm()
        login_form = AuthenticationForm()

    return render(request, 'malware.html', locals())


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None and user.is_active:
                auth.login(request, user)

    return HttpResponseRedirect('/malwareupload/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/malwareupload/')
