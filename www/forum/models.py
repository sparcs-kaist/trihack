from django.db import models

# Create your models here.

class Post(models.Model):
	title = models.CharField("Title", max_length=100)
	text = models.TextField("Contents")
	hits = models.IntegerField(null=True, blank=True)
	like = models.IntegerField(null=True, default=0)
	hate = models.IntegerField(null=True, default=0)

	def _str_(self):
		return self.title
