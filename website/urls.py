from django.conf.urls import patterns, include, url

import feature.urls

# Imported for the side effect of registering all feature flippers.
import photos.views
import photos.models

urlpatterns = patterns('',
    url(r'^feature/', include('feature.urls')),
    url(r'^details/(?P<photo_id>\d+)$', 'photos.views.details'),
    url(r'^buy$', 'photos.views.buy'),
    url(r'^checkout$', 'photos.views.checkout'),
    url(r'^admin/purchase_log$', 'photos.views.purchase_log'),
    url(r'^$', 'photos.views.index'),
)
