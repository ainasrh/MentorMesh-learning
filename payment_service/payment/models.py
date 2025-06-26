from django.db import models

# Create your models here.


from django.db import models

class Payment(models.Model):
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
