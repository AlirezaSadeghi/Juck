from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings

admin.autodiscover()

# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'juck.accounts.views.homepage', name='homepage'),

                       url(r'', include('juck.accounts.urls')),
                       url(r'^accounts/', include('juck.accounts.urls')),
                       url(r'^news/', include('juck.news.urls')),
                       url(r'^article/', include('juck.articles.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        url(r'^captcha/', include('captcha.urls')),
                        url(r'^/images/favico', RedirectView.as_view(url=settings.STATIC_ROOT + 'images/favicon.ico'), )

)
