from django.db import models



class Course(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    trainer = models.IntegerField()
    price =models.DecimalField(max_digits=8,decimal_places=2)
    video =models.FileField(upload_to='course_videos/',blank=True,null=True)
    is_published = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    user = models.IntegerField()
    course = models.ManyToManyField(Course)
    enrolled_at = models.DateTimeField(auto_now_add=True)
        