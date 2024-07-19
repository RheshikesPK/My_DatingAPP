from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register2/', Register2View.as_view(), name='register2'),
    path('register3/', EmploymentDetailsView.as_view(), name='register3'),
    path('register4/', Register4View.as_view(), name='register4'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('myprofile/<int:pk>/', MyProfileView.as_view(), name='myprofile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-view'),
    path('address/', AddressCreateView.as_view(), name='address'),
    path('send_message/<int:id>/', SendMessageView.as_view(), name='send_message'),
]