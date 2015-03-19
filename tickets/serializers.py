from rest_framework import serializers
from tickets.models import Ticket
from django.contrib.auth.models import User

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticket
        fields = ('url', 'owner',
                  'created', 'title', 'description', 'progress', 'priority', 'hardness')
                  
class UserSerializer(serializers.HyperlinkedModelSerializer):
    tickets = serializers.HyperlinkedRelatedField(queryset=Ticket.objects.all(), view_name='ticket-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'tickets')
