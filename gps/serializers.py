from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from gps.models import GpsNode, GpsNodeMetrics

import pdb

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    #nodes = serializers.PrimaryKeyRelatedField(many=True, 
    #              queryset=GpsNode.objects.all())
    nodes = serializers.HyperlinkedRelatedField(many=True, 
                view_name='gpsnode-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'nodes') 

class GpsNodeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = GpsNode
        fields = ('url', 'id', 'user', 'ident', 
                    'created', 'lastActive', 'was_active_recently')

class GpsNodeMetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GpsNodeMetrics
        fields = ('url', 'id', 'vin', 'vinCached', 'latitude', 'longitude',
                  'accuracy', 'speed', 'altitude', 'nsTimestamp', 'bearing', 'node')

