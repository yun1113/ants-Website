from django.conf.urls import url
from django.contrib import admin
from malwaredb.views import malware_search, index, malware_detail, \
    malware_download, load_hooklog_page, contact, malware_family, malware_behavior, \
    CustomObtainExpiringAuthToken, SubmitFileView, GetHooklogView
from user_account.views import logout
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.conf import settings


handler404 = 'malwaredb.views.bad_request'
handler500 = 'malwaredb.views.server_error'

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^index/$', index, name='index'),  # login, signup, upload

    url(r'^malwaredb/$', malware_search),  # search
    url(r'^malwaredetail/$', malware_detail),  # detail
    url(r'^malwaredownload/$', malware_download),  # download

    url(r'^malwarefamily/$', malware_family),
    url(r'^malwarebehavior/$', malware_behavior),

    url(r'^contact/$', contact),
    url(r'^logout/$', logout, name='log-out'),

    # api
    url(r'^request_token/', CustomObtainExpiringAuthToken.as_view()),
    url(r'^submit_file/', SubmitFileView.as_view()),
    url(r'^get_hooklog/', GetHooklogView.as_view()),


    url(r'^analysis/(?P<hash_value>\w+)/(?P<page>\w+)$', load_hooklog_page),  # detail hooklog tab
    # url(r'^virustotal/(?P<hash>\w+)/$', loadvt),
]

# media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)