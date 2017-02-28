from django.conf.urls import url, handler400, handler403, handler404, handler500
from django.contrib import admin

from malwaredb.views import malware_search, get_index, malware_detail, \
    malware_download, load_hooklog_page, contact, malware_family, malware_behavior
from user_account.views import logout


handler404 = 'malwaredb.views.bad_request'
handler500 = 'malwaredb.views.server_error'

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^index/$', get_index),  # login, signup, upload

    url(r'^malwaredb/$', malware_search),  # search
    url(r'^malwaredetail/$', malware_detail),  # detail
    url(r'^malwaredownload/$', malware_download),  # download

    url(r'^malwarefamily/$', malware_family),
    url(r'^malwarebehavior/$', malware_behavior),

    url(r'^contact/$', contact),
    url(r'^logout/$', logout),

    url(r'^analysis/(?P<hash_value>\w+)/(?P<page>\w+)$', load_hooklog_page),  # detail hooklog tab
    # url(r'^virustotal/(?P<hash>\w+)/$', loadvt),
]
