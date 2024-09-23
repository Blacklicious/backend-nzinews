from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from news.models import Job
from news.serializers import JobSerializer
from users.models.businesses import Business

# List all jobs or create a new job
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])  # Authenticated users can create, everyone can list
def job_list_create(request):
    if request.method == 'GET':
        # Get all jobs
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new job
        data = request.data.copy()
        data['created_by'] = request.user.id  # Set the user as the creator
        serializer = JobSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_jobs(request):
    if request.method == 'GET':
        # Get all jobs
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    data = request.data.copy()
    data['created_by'] = request.user.id  # Automatically assign the creator
    print('data---->', data.get('businessId'))



    # Create a job serializer and validate the data
    serializer = JobSerializer(data=data)
    print('serializer---->' , serializer)
    if serializer.is_valid():
        # Save the job with the company (business) attached
        serializer.save()  # Here we associate the business with the company field
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a job
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])  # Authenticated users can modify, everyone can view
def job_detail(request, pk):
    # Get the job by ID
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'GET':
        # Retrieve job details
        serializer = JobSerializer(job)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update job (only if the user is the creator or an admin)
        if request.user != job.created_by and not request.user.is_staff:
            return Response({'error': 'You are not authorized to update this job.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['created_by'] = request.user.id  # Ensure the creator is preserved
        serializer = JobSerializer(job, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete job (only if the user is the creator or an admin)
        if request.user != job.created_by and not request.user.is_staff:
            return Response({'error': 'You are not authorized to delete this job.'}, status=status.HTTP_403_FORBIDDEN)

        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Activate a job
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user != job.created_by and not request.user.is_staff:
        return Response({'error': 'You are not authorized to activate this job.'}, status=status.HTTP_403_FORBIDDEN)

    job.status = 'active'
    job.save()
    return Response({'status': 'Job activated'})


# Deactivate a job
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user != job.created_by and not request.user.is_staff:
        return Response({'error': 'You are not authorized to deactivate this job.'}, status=status.HTTP_403_FORBIDDEN)

    job.status = 'inactive'
    job.save()
    return Response({'status': 'Job deactivated'})