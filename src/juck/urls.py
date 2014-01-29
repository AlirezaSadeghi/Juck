from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^$', 'juck.accounts.views.homepage', name='homepage'),

                       url(r'', include('juck.accounts.urls')),
                       url(r'', include('social_auth.urls')),
                       url(r'^accounts/', include('juck.accounts.urls')),
                       url(r'^news/', include('juck.news.urls')),
                       url(r'^article/', include('juck.articles.urls')),
                       url(r'^question/', include('juck.question.urls')),
                       url(r'^requests/', include('juck.requests.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT,
                          'show_indexes': True}),
)

urlpatterns += patterns('',
                        url(r'^captcha/', include('captcha.urls')),
                        url(r'^/images/favico', RedirectView.as_view(url=settings.STATIC_ROOT + 'images/favicon.ico'), )

)
