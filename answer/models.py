from __future__ import unicode_literals
from django.db import models

class Input(models.Model):   # class for taking input
    ques = models.CharField(max_length=50)

    # inner meta class shows information about model
    class Meta:
        db_table = 'Input'
