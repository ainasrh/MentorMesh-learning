from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns =[
    path('create/',CreateCourseAPI.as_view(),name="create-course"),
    path('course-video/',CourseVideoCreateAPI.as_view(),name='create-video'),
    path('delete/<int:pk>/',DeleteCourseAPI.as_view(),name='delete-course'),
    path('courses/',GetCourseAPI.as_view(),name='course-list'),    
    path('courses/<int:pk>/',GetCourseAPI.as_view(),name='course-detail'),
    path('update/<int:pk>/',UpdateCourseAPI.as_view(),name='update-course'),
    path('enroll/',EnrollCourseAPI.as_view(),name='enroll-course'),
    path('progress/<int:video_id>/',UpdatePartProgressAPI.as_view(),name='update-progress'),
    path('progress/',UpdatePartProgressAPI.as_view(),name='get-progress'),

    path('trainerdata/',CourseCreateView.as_view())
    

    

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
