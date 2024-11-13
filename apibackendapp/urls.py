from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


#create an instance of the Defaultrouter class
router = DefaultRouter()

#register the mapping for urls And views
#r for raw string to escape special charcter
router.register(r'departments',views.DepartmentViewSet)
router.register(r'employee',views.EmployeeViewSet)
router.register(r'users',views.UserViewSet)

#creating the urls for the login and signup API views
#they are not viewset they are API views
#URL patterns list directly

urlpatterns = [
    path("Signup/",views.SignupAPIView.as_view(),name="user-signup"),
    path("Login/",views.LoginAPIView.as_view(),name="user-Login"),
]

#create a urlpattern list from the router urls
urlpatterns = urlpatterns + router.urls
