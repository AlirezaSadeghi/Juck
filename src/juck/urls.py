from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'juck.accounts.views.homepage', name='homepage'),

                       url(r'', include('juck.accounts.urls')),
                       url(r'^accounts/', include('juck.accounts.urls')),
                       url(r'^news/', include('juck.news.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)