from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.generics import get_object_or_404
import logging
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import MultiPartParser,FormParser


logger=logging.getLogger(__name__)




# Course APIs



        
class CreateCourseAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self,request):

        logger.info(f"data from front {request.data}")
        serialized = courseSerializer(data=request.data,context={"request":request})
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    



# Course video Create
class CourseVideoCreateAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        logger.info(f"video request data {request.data}")
        serializer = CourseVideoSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        try:

            data=CourseVideo.objects.all()
            serialized=CourseVideoSerializer(data,many=True)
            return Response(serialized.data,status=status.HTTP_200_OK)
        except CourseVideo.DoesNotExist:
            return Response({'error':'product not found'},status=status.HTTP_404_NOT_FOUND)
# Get courses 

# trending courses
class TrendingCourseAPI(APIView):
    def get(self, request):
        trending = Course.objects.filter(is_trending=True)[:3]
        serialized = courseSerializer(trending, many=True, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)

# get courses     
class GetCourseAPI(APIView):

    def get(self,request,pk=None):       
        if pk :
            data = get_object_or_404(Course,id=pk)
            serialized = courseSerializer(data,context={'request':request})
        else:
            data=Course.objects.all().order_by("id")

            serialized = courseSerializer(data,many=True,context={'request':request})

        return Response(serialized.data,status=status.HTTP_200_OK)

# get courses based on Trainer

class GetCourseBasedTrainer(APIView):
    def get(self,request):
        logger.info(f"{request.user}")
        courses=Course.objects.filter(trainer=request.user.id)
        serializer=courseSerializer(courses,many=True,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class UpdateCourseAPI(APIView):
    def patch(self,request,pk):
        # logger.info(request.data)
        
        try:
            course_data=Course.objects.get(id=pk)
            
        except Course.DoesNotExist:
            return Response({'error':'prodcut not found'},status=status.HTTP_404_NOT_FOUND)
        
        
        serialized=courseSerializer(course_data,data=request.data,partial=True,context={"request":request})

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_200_OK)
        else: 
            logging.error(serialized.errors)  # Add this for debugging
            return Response({'error':"data is not valid "},status=status.HTTP_400_BAD_REQUEST)

class DeleteCourseAPI(APIView):
    
    def delete(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
            course.delete()
            return Response({'message': 'Course deleted successfully'}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
# Enrollment 

class EnrollCourseAPI(APIView):
    def post(self,request):
        serialized=EnrollmentSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()

            # taking currentlly saved object
            enrollment=serialized.instance
            # filtering course videos based on passed course id 
            course_videos=CourseVideo.objects.filter(course=enrollment.course)

            EnrollmentPartProgress.objects.bulk_create([
                EnrollmentPartProgress(enrollment=enrollment,video=video)
                for video in course_videos
            ])
            return Response(serialized.data,status=status.HTTP_201_CREATED)
        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UpdatePartProgressAPI(APIView):
    def get(self,requst,video_id=None):
        
        if video_id:
            progress_entries = EnrollmentPartProgress.objects.filter(video=video_id)
            if not progress_entries.exists():
                return Response({'error': "Progress report not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            progress_entries = EnrollmentPartProgress.objects.all()
        
        serializer = EnrollmentProgressSerializer(progress_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self,request,video_id):
        try:
            part =EnrollmentPartProgress.objects.get(id=video_id)
        except EnrollmentPartProgress.DoesNotExist:
            return Response({'error': 'Part progress not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnrollmentProgressSerializer(part,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


