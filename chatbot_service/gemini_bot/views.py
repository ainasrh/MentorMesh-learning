from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .gemini_client import get_gemini_response
from rest_framework import status
import logging
logger = logging.getLogger(__name__)


# Create your views here.


class GeminiChatView(APIView):
    def post(self, request):
        print("gemini view worked ")
        message = request.data.get("message")

        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reply = get_gemini_response(message)
            logger.info(f"gemini response : {reply}")
            return Response({"response": reply}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Gemini API error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
