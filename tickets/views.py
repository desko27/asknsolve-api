from django.contrib.auth.models import User
from rest_framework import permissions
# from rest_framework import renderers
from rest_framework import viewsets
# from rest_framework.decorators import detail_route
# from rest_framework.response import Response
from tickets.models import Ticket
from tickets.permissions import IsOwnerOrReadOnly
from tickets.serializers import TicketSerializer, UserSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents user tickets.
    The **owner** of the ticket may update or delete instances
    of the ticket.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.
    As you can see, the collection of ticket instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
