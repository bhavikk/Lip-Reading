from django.db import models
from django import forms
from django.conf import settings
import os

class Video(models.Model):
	file = models.FileField(upload_to='videos/')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.file.name)
	
	def delete(self, *args, **kwargs):
		os.remove(self.file.path)
		super(Video,self).delete(*args,**kwargs)
	
	def __str__(self):
		return self.file.name
