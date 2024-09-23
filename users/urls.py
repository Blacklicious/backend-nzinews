from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views.users import get_user
from .views.members import create_member, get_member, update_member, delete_member
from .views.businesses import get_businesses, create_business, get_business, update_business, delete_business
from .views.employees import get_employees, create_employee, get_employee, update_employee, delete_employee, get_employees_application
from .views import RegisterView, CustomTokenObtainPairView

router = DefaultRouter()

urlpatterns = [
    path('register/api/', RegisterView.as_view(), name='register'),
    path('login/api/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/get/', get_user, name='get_user'),
    #--------------------------------------------------------------------------------
    path('members/api/', create_member, name='create_member'),
    path('member/api/get/', get_member, name='get_member'),
    path('member/api/update/', update_member, name='update_member'),
    path('member/api/delete/', delete_member, name='delete_member'),
    #--------------------------------------------------------------------------------
    path('businesses/api/', get_businesses, name='get_businesses'),
    path('business/api/', create_business, name='create_business'),
    path('business/api/get/', get_business, name='get_business'),
    path('business/api/update/', update_business, name='update_business'),
    path('business/api/delete/', delete_business, name='delete_business'),
    #--------------------------------------------------------------------------------
    path('employees/api/', get_employees, name='get_employees'),
    path('employee/api/', create_employee, name='create_employee'),
    path('employee/api/get/', get_employee, name='get_employee'),
    path('employee/api/update/', update_employee, name='update_employee'),
    path('employee/api/delete/', delete_employee, name='delete_employee'),
    #path('employees/applications/api/', get_employees_applications, name='get_employees_applications'),
    path('employees/application/<int:pk>/api/', get_employees_application, name='get_employees_application'),
    #path('employee/application/<int:pk>/api/', get_employee_application, name='create_employee_application'),
    #--------------------------------------------------------------------------------
    path('', include(router.urls)),  # Include the router's URLs
]