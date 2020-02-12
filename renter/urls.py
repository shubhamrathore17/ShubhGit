from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from renter.views import *

urlpatterns = [
    path('register/', register, name='register'),

    path('login/', login, name='login'),
    
    path('logout/', auth_views.logout, {'next_page': '/login/'}, name='logout'),

 	path('home/', home, name='home'),

 	path('profile/<int:profile_id>/', profile_page, name='profile_page'),

 	path('profile/', profile_page_rental, name='profile_page_rental'),

 	path('artical/', property, name='property'),

 	path('delete_property/<int:property_id>', delete_property,name='delete_property'),

 	path('artical/<int:property_id>/', property_detail, name="property_detail"),

	path('apply_for_property/<int:property_id>/', apply_for_property, name="apply_for_property"),

 	path('password/', change_password, name='change_password'),

	path('forgot_password/',ForgotPassword.as_view(),name='forgot_password'),

 	path('edit_property/<int:pk>/', PropertyUpdateView.as_view(), name='edit_property'),

 	# for class:-

 	path('api/',ProfileList.as_view(),name='api')

 	#FOR METHOD ONLY:-

 	# path('api/profile_list/',profile_list,name='profile_data_list')
]

