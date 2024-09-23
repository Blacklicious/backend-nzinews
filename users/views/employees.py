from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ..serializers import EmployeeSerializer, UserSerializer
from ..models import Employee
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|

@api_view(['GET'])
def get_employees(request):
    employees = Employee.objects.all()
    if employees.exists():
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employee(request):
    # Log the incoming data for debugging purposes
    print("Incoming data:", request.data)

    # Initialize the serializer with the request data and include the request context
    serializer = EmployeeSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # Save the Employee with the authenticated user automatically set
        serializer.save(user=request.user)
        # Log the created Employee for debugging
        print("Employee created:", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # Log errors if the data is not valid
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|
#--------------------------------------------------------------------------------|

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_employees_application(request, pk):
    try:
        # Filter employees based on the job and role
        job_hunters = Employee.objects.filter(job_nzid=pk, role='job_hunter')
        serialized_jobhunters = []
        # Check if any job hunters exist
        if job_hunters.exists():
            # Fetch and serialize the associated images for the job_hunter
            for job_hunter in job_hunters:
                jobhunter_serializer = EmployeeSerializer(job_hunter).data
                user = User.objects.filter(id=job_hunter.user.id).first()
                user_serializer = UserSerializer(user).data
                jobhunter_with_data = {
                    **jobhunter_serializer,
                    'user': user_serializer,
                }
                serialized_jobhunters.append(jobhunter_with_data)
            
            return Response(serialized_jobhunters, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No job hunters found for this job'}, status=status.HTTP_404_NOT_FOUND)

    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
    
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
