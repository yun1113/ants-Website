from django.http import HttpResponseRedirect
from django.contrib import auth

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')
