from django.db import models
import mytoolkit
from django.contrib.auth.models import User


class Document(models.Model):
    docfile = models.FileField(upload_to='downloads')
    date_add = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
