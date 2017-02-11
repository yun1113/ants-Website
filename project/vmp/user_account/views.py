from django.shortcuts import render
from django.db.models import Q

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

    return render(request, 'malware.html', locals())