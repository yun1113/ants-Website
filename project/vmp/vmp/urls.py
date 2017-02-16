from django.conf.urls import url
from django.contrib import admin
from malwaredb.views import malware_search, malware_upload, malware_detail, \
    malware_download, load_hooklog_page, contact, malware_family, malware_behavior, \
    SubmitFileView, GetHooklogView
from user_account.views import register, logout, login
from rest_framework.authtoken import views as get_token_view
from django.conf.urls import handler400, handler403, handler404, handler500

handler404 = 'malwaredb.views.bad_request'
handler500 = 'malwaredb.views.server_error'

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^malwareupload/$', malware_upload),  # upload
    url(r'^malwaredb/$', malware_search),  # search
    url(r'^malwaredetail/$', malware_detail),  # detail
    url(r'^malwaredownload/$', malware_download),  # download
    url(r'^malwarefamily/$', malware_family),
    url(r'^malwarebehavior/$', malware_behavior),
    # url(r'^malwarefamily2/$', malware_family2),
    url(r'^contact/$', contact),

    url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^logout/$', logout),

    # api
    url(r'^request_token/', get_token_view.obtain_auth_token),
    url(r'^submit_file/', SubmitFileView.as_view()),
    url(r'^get_hooklog/', GetHooklogView.as_view()),


    url(r'^analysis/(?P<hash_value>\w+)/(?P<page>\w+)$', load_hooklog_page),  # detail hooklog tab
    # url(r'^virustotal/(?P<hash>\w+)/$', loadvt),
]
