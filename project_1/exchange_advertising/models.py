from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class advertising(models.Model):
    id = models.AutoField(primary_key= True)
    description = models.CharField(max_length=256)
    email = models.CharField(max_length=128)
    # 1:confirmed, 2: review queue, 3: Not confirmed
    state = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(3)], null=True,default=2) 
    category = models.CharField(max_length=128, null=True)
    image = models.CharField(max_length=256, null=True, blank=True)





