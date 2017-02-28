from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from datetime import datetime

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(blank=False)

    def __unicode__(self):
        return unicode(self.user)


class AuditEntry(models.Model):

    user = models.ForeignKey(User)
    ip = models.GenericIPAddressField(null=True)
    action = models.CharField(max_length=64)
    action_date = models.DateTimeField()

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, user=user, action_date=datetime.now())


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, user=user, action_date=datetime.now())
