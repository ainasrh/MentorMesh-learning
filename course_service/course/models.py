from django.db import models



class Course(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    trainer = models.IntegerField()
    price =models.DecimalField(max_digits=8,decimal_places=2)
    is_published = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)


class CourseVideo(models.Model):
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  
    video = models.FileField(upload_to='course_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    user = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments',null=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('user', 'course')


class EnrollmentPartProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='parts')
    video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE)  
    progress = models.CharField(max_length=20, choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='not_started')
    last_watched_at = models.DateTimeField(null=True, blank=True)
    
