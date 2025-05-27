from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status




class CreateCourseAPI(APIView):
    
    def post(self,request):
        serialized = courseSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_200_OK)
        return Response({'error':'data is not valid'},status=status.HTTP_400_BAD_REQUEST)
    
        