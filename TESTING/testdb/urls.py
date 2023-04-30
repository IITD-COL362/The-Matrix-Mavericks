from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
	# path('city-list/', views.city_list, name='city_list'),
	# path('meal-count/', views.meal_count, name='meal_count'),
	path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('add-rest/', views.add_restaurant, name='add_rest'),
	path('trending/', views.trending, name='trending'),
	path('restaurants/<str:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
	path('restaurants/<str:restaurant_id>/menu/', views.menu, name='menu'),
    path('restaurants/<str:restaurant_id>/rate-rest/', views.rate_restaurant, name='rate_restaurant'),
    path('restaurants/<str:restaurant_id>/menu/<str:food_id>/<str:meal_type>/', views.track_meal, name='track'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('dashboard/add_meal/', views.add_meal, name='add_meal'),
	path('dashboard/stats/',views.statistics_user, name = 'statistics_user'),
	path('close_rest/', views.restaurants_nearme, name='restaurants_nearme'),
	path('profile/', views.profile_user, name='profile'),
	path('profile/update_weight/',views.update_weight, name = 'update_weight'),
	path('profile/update_mailid/',views.update_mailid, name = 'update_mailid'),
	path('profile/update_city/',views.update_city, name = 'update_city'),
	path('profile/update_address/',views.update_address, name = 'update_address'),
	path('profile/update_phonenumber/',views.update_phonenumber, name = 'update_phonenumber'),
	path('restaurant_search/', views.filter_restaurant,name='filter_restaurant'),
	path('food/', views.filter_food,name='filter_food'),
	path('mix/', views.filter_mix,name='filter_mix')
]
