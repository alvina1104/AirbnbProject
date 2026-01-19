from django.urls import path,include
from .views import (UserProfileListAPIView,UserProfileDetailAPIView,
                    CityListAPIView,CityDetailAPIView,
                    PropertyListAPIView,PropertyDetailAPIView,
                    BookingViewSet,ReviewCreateAPIView,PropertyViewSet,
                    RegisterView,LoginView,LogoutView)
from rest_framework import routers



router = routers.SimpleRouter()
router.register(r'booking',BookingViewSet)
router.register(r'property_create',PropertyViewSet)



urlpatterns =[
    path('',include(router.urls)),
    path('property/',PropertyListAPIView.as_view(),name='property_list'),
    path('property/<int:pk>/',PropertyDetailAPIView.as_view(),name='property_detail'),
    path('cities/',CityListAPIView.as_view(),name='city_list'),
    path('cities/<int:pk>/',CityDetailAPIView.as_view(),name='city_detail'),
    path('user/',UserProfileListAPIView.as_view(),name='user_profile_list'),
    path('user/<int:pk>/',UserProfileDetailAPIView.as_view(),name='user_profile_detail'),
    path('review/',ReviewCreateAPIView.as_view(),name='review_create'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
]