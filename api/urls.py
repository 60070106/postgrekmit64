from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'
urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('event/register/', EventView.as_view(), name='event_register'),
    path('event/get_all_event/', GetAllEventView.as_view(), name='event_all'),
    path('event/get/detail/', GetEventDetail.as_view(), name='event_detail'),
    path('event/camp/register/', RegisterEvent.as_view(), name='camp_register'),
    path('event/camp/people/', GetEventPeople.as_view(), name='camp_people'),
    path('event/camp/attendance/', GetEventAvaliableCheckin.as_view(), name='camp_attendance'),
    path('event/camp/check/', EventView.as_view(), name='camp_checkin')
]

# GetAllEventView