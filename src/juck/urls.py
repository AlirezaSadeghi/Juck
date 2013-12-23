from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.static import serve
from juck.settings import MEDIA_ROOT
from django.conf import settings

admin.autodiscover()




urlpatterns = patterns('',
                       url(r'^$', 'juck.accounts.views.homepage', name='homepage'),

                       url(r'', include('juck.accounts.urls')),
                       url(r'^accounts/', include('juck.accounts.urls')),
                       url(r'^news/', include('juck.news.urls')),
                       url(r'^admin/', include(admin.site.urls)),

)


urlpatterns += patterns('',
   (r'^media/(?P<path>.*)$', 'django.views.static.serve',
   {'document_root': settings.MEDIA_ROOT,
   'show_indexes' : True}),
)