from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

from ckeditor.fields import RichTextField

class Post(models.Model):
  title = models.CharField(max_length=40)
  book_author = models.CharField(max_length=50)
  image = models.ImageField(default='default.jpg', upload_to='photos/%Y/%m/%d/')
  content = RichTextField()
  book_published = models.DateField(default=datetime.now, blank=False)
  date_posted = models.DateTimeField(default=datetime.now, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})

  
  # def save(self, *args, **kwargs):
  #   super(Post, self).save(*args, **kwargs)

  #   img = Image.open(self.image.path)

  #   if img.height > 300 or img.width > 300:
  #     output_size = (300, 300)
  #     img.thumbnail(output_size)
  #     img.save(self.image.path)
