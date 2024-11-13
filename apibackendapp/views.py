from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee,Department
from .serializers import EmployeeSerializer,DepartmentSerializer,UserSerializer,LoginSerializers,SignupSerializer
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

from rest_framework import status

# Create your views here.

class SignupAPIView(APIView):
    permission_classes = [ AllowAny] #Signup doesnot need logging in 
    #defining post fn to handle signup post data
    def post(self,request):
        #create an object for  the Signup Serializer
        #by giving the data received to its constructor 
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            #createv  a new user if the serializer is valid
            user = serializer.save() #will give back a token for the user
            
            token,created = Token.objects.get_or_create(user=user) #will give back token obj
            #once the user is created,give back the response with usrid,usrname,token,group
            return Response({
                "user_id": user.id,
                "username":user.username,
                "role":user.groups.all()[0].id if user.groups.exists() else None, #give back the first group id of the user if role/group exits
                "data":{
                        "Token":token.key
                        }
            },status=status.HTTP_201_CREATED)
        else:
            response = { 'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
            
#create an APIView for Login


class LoginAPIView(APIView):

    permission_classes = [AllowAny] #login does not need logging in
    #defining post fin' to handle signup post request data:
    def post(self, request):
    #create an object for the LoginSerializer
    #by giving the data received to its constructor
        serializer=LoginSerializers(data=request.data)
        if serializer.is_valid():
            #get the username, pasword from the validated data
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            #try to authenticate the user using this username and password
            #if successfully authenticated, it will return back a valid user object

            user = authenticate(request, username=username, password=password)
            

            if user is not None:
                token = Token.objects.get(user=user)
                response = { 
                            "status":status.HTTP_200_OK,
                            "message":"success",
                            "username":user.username,
                            
                            "role":user.groups.all()[0].id if user.groups.exists() else None,
                            "data":{
                                "Token":token.key
                            }
                        }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid username or password",
                    
                }
                return Response (response, status.HTTP_401_UNAUTHORIZED)    
        else:
            response = { 'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    
    
#create viewsets class inheriting the Model ViewSet class
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()#get all objects ofthe model
    serializer_class=DepartmentSerializer #and render it using this serializer
    #permission_classes= []
    permission_classes = [IsAuthenticated] #to restrict for login users
    
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()#get all objects ofthe model
    serializer_class=EmployeeSerializer #and render it using this serializer
    filter_backends = [filters.SearchFilter]
    search_fields= ['EmployeeName','Designation']
    permission_classes = []
    #permission_classes = [IsAuthenticated] #to restrict for login users
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()#get all objects ofthe model
    serializer_class=UserSerializer #and render it using this serializer
    permission_classes = []
    #permission_classes = [IsAuthenticated] #to restrict for login users
    