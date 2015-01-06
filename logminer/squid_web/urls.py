from django.conf.urls import patterns, include, url

from django.contrib import admin
from web1.views	import *
from rizhi.views	import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'squid_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^index$', index),
    url(r'^main/', main),
    url(r'^getlog', get_log),
    url(r'^cartoon$', cartoon),
    url(r'^signin$', login_view),
    url(r'^logout$', logout_view),
)
