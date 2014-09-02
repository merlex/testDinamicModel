from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testwork.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'myapp.views.index', name='index'),
    url(r'^(?P<model>\w+)/$', 'myapp.views.view', name='view'),
    url(r'^json/(?P<model>\w+)/$', 'myapp.views.json', name='json'),
    url(r'^save/(?P<model>\w+)/$', 'myapp.views.save', name='save'),
    url(r'^create/(?P<model>\w+)/$', 'myapp.views.create', name='create'),

)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
