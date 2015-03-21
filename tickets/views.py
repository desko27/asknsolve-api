from asknsolve.keys import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import permissions
# from rest_framework import renderers
from rest_framework import viewsets
# from rest_framework.decorators import detail_route
from tickets.models import Ticket
from tickets.permissions import IsOwnerOrReadOnly
from tickets.serializers import TicketSerializer, UserSerializer
from oauth2client.client import OAuth2WebServerFlow

@api_view(['POST'])
@parser_classes((JSONParser,))
def login(request):
    if request.method == 'POST':
        
        # request auth url
        flow = OAuth2WebServerFlow(client_id = GOOGLE_CLIENT_ID,
                           client_secret = GOOGLE_CLIENT_SECRET,
                           scope = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
                           redirect_uri = request.data['redirect_uri'])
        
        return Response({'url': flow.step1_get_authorize_url()})

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
