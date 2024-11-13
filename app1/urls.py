from django.urls import path,include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router=routers.DefaultRouter()
router.register(r'eventticket',EventTicketViewSet)
router.register(r'signup',UserViewSet)
router.register(r'turfbook',TurfBookingViewSet)


urlpatterns = [
    path('home/', contact_form, name='contact-form'),
    path('book/', book_slot, name='book_slot'),
    path('ticket/<int:booking_id>/',ticket,name='ticket'),
    path('events/',event_ticket,name='event_ticket'),
    path('login/', LoginView.as_view(), name='login'),
    path('',include(router.urls)),
    #  path('api/token/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
     path('turfbookings/<int:user_id>/', TurfDetailsUser.as_view(), name='turf_bookings'),
     path('eventbookings/<int:user_id>/',EventDetailsUser.as_view(),name='event_booking')
   
 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
