from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from .models import Department,Employee
from datetime import date
from django.urls import reverse
from .serializers import EmployeeSerializer
from rest_framework import status

# Create your tests here.
#creating new employeeviewsettest class inheriting the APITestCase class
class EmployeeViewSetTest(APITestCase):
    #defining a function to setup some basic data for testing
    def setUp(self):
        #create a sample department object
        self.department = Department.objects.create(DepartmentName="HR")
        #create a sample employee objects and assign the department
        self.employee = Employee.objects.create(
            EmployeeName = "Jackie Chan",
            Designation = "KUNGFU MASTER",
            DateOfJoining = date(2024,11,13),
            DepartmentID = self.department,
            Contact = "China",
            IsActive = True
        )
        #since we are testing API, we need to create an APIClient object
        self.client = APIClient()
    #defining function to test employee listing api /endpoint 
    def test_employee_list(self):
        #the default reverse url for listing modelname-list
        url = reverse('employee-list')
        response = self.client.get(url) #send the api and get the response
        #get all the employee objects
        employee = Employee.objects.all()
        #creates a serializer 
        serializer = EmployeeSerializer(employee, many=True)
        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #check if status is 200
        self.assertEqual(response.data ,serializer.data)         
        
        
           #defining function to test employee listing api /endpoint 
    def test_employee_details(self):
        #the default reverse url for listing modelname-list
        url = reverse('employee-detail',args= [self.employee.EmployeeId])
        response = self.client.get(url) #send the api and get the response
        #creates a serializer 
        serializer = EmployeeSerializer(self.employee)
        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #check if status is 200
        self.assertEqual(response.data,serializer.data)         
        
        