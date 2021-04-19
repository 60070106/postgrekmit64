from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'
urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('event_register/', EventView.as_view(), name='event_register'),
    path('get_all_event/', GetAllEventView.as_view(), name='event_all'),
    path('event_get_detail/', GetEventDetail.as_view(), name='event_detail'),
    path('event_camp_register/', RegisterEvent.as_view(), name='camp_register'),
    path('event_camp_people/', GetEventPeople.as_view(), name='camp_people'),
    path('event_camp_attendance/', GetEventAvaliableCheckin.as_view(), name='camp_attendance'),
    path('event_camp_check/', EventCheckView.as_view(), name='camp_checkin'),
    path('event_approver_check/', EventApproverView.as_view(), name='approver_event'),
    path('event_edit/', EditEventDetail.as_view(), name='event_edit')
]

# GetAllEventView