from django.conf.urls import url
from django.contrib import admin
from malwaredb.views import malwarelist, malwareupload, loadpage, loadvt
from django.conf.urls import handler400, handler403, handler404, handler500

handler404 = 'malwaredb.views.bad_request'
handler500 = 'malwaredb.views.server_error'

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^malwareupload/$', malwareupload), # upload
    url(r'^malwaredb/$', malwarelist), # search
    url(r'^load/(?P<hash>\w+)/$', loadpage), 
    url(r'^virustotal/(?P<hash>\w+)/$', loadvt),
]
