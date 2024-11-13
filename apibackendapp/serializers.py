from rest_framework import serializers #import module
from .models import Employee,Department
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=False)
    def create(self, validated_data):
        group_name = validated_data.pop("group_name",None)
        validated_data['password'] = make_password(validated_data.get("password"))
        user = super(SignupSerializer,self).create(validated_data)
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

    class Meta:
         model = User
         fields = ['username', 'password', 'group_name']

class LoginSerializers(serializers.ModelSerializer):
    #creating custom fields for username
    username = serializers.CharField()
    class Meta:
        model = User
        fields =['username', 'password']

    

    

#create serializer by inheerting model serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: #will provide metedata to the model
        model = Department
        fields = ('DepartmentID','DepartmentName')
        
        
def name_validation(employee_name):
    if len(employee_name)<3:
        raise serializers.ValidationError("Name must be atleast 3 char")
    return employee_name
class EmployeeSerializer(serializers.ModelSerializer):
    #Department is a custom field in this serializer
    #sources Departmentid says that the field should get data about
    #the DepartmentID of that employee in the model
    Department = DepartmentSerializer(source='DepartmentID',read_only=True)
    EmployeeName =serializers.CharField(max_length=200 , validators=[name_validation])
    class Meta:
        model=Employee
        fields=('EmployeeId','EmployeeName','Designation','DateOfJoining','IsActive','DepartmentID','Department')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username') #get only these two fields