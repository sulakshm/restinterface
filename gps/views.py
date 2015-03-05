from django.shortcuts import render
from django.contrib.auth.models import User
from gps.models import GpsNode, GpsNodeMetrics
from gps.permissions import IsOwnerOrNone, IsOwnerOrReadOnly
from rest_framework import generics, viewsets, permissions

from gps.serializers import UserSerializer, GpsNodeSerializer, GpsNodeMetricSerializer

# Create your views here.
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class GpsNodeViewSet(viewsets.ModelViewSet):
    model = GpsNode
    #queryset = GpsNode.objects.all()
    serializer_class = GpsNodeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_anonymous():
            return
        return GpsNode.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print "Viewset: GpsNode.perform_create %r" %repr(self.request)
        serializer.save(user=self.request.user)

class GpsNodeMetricViewSet(viewsets.ModelViewSet):
    #queryset = GpsNodeMetrics.objects.all()
    serializer_class = GpsNodeMetricSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print 'get_queryset() %s' % self.request.user.is_anonymous()
        if self.request.user.is_anonymous():
            return
        nodes = GpsNode.objects.filter(user=self.request.user)
        import pdb; pdb.set_trace()
        return GpsNodeMetrics.objects.filter(node__in=nodes)

    def perform_create(self, serializer):
        print "Viewset: GpsNodeMetric.perform_create %r" %repr(self.request)
        #serializer.save(user=self.request.user)
        import pdb; pdb.set_trace()

class GpsNodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GpsNode.objects.all()
    serializer_class = GpsNodeSerializer
