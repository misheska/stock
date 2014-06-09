from django.conf.urls import patterns, include, url

urlpatterns = patterns('feature.views',
    url(r'^set_enabled$', 'set_enabled'),
    url(r'^$', 'index'),
)
