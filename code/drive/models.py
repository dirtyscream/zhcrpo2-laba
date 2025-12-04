from django.db import models


class File(models.Model):
    file_id = models.CharField(max_length=36)
    file_name = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    cid = models.CharField(max_length=200)
