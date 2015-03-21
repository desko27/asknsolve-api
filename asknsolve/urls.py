from tickets import views
from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^', include('tickets.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
