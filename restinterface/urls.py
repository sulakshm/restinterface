from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User

from django.contrib import admin

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from gps.views import UserViewSet, GpsNodeViewSet, GpsNodeMetricViewSet

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'gps', GpsNodeViewSet, base_name='gpsnode')
router.register(r'gpsmetrics', GpsNodeMetricViewSet, base_name='gpsnodemetrics')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


"""
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'restinterface.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
"""
