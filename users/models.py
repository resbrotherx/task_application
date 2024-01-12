from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django import forms
from django.contrib.auth.models import AbstractUser
# from Template.models import User

# class ProfileInfo(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	mobile = models.IntegerField(blank=True,null=True)
# 	def __str__(self):
# 		return f'{self.user.username} info'



# class User(AbstractUser):
#     email = models.EmailField(unique=True, null=True)
#     username = models.CharField(max_length=10000)
#     is_student = models.BooleanField(default=True)
#     is_teacher = models.BooleanField(default=False)
#     verified = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
	

#     def __str__(self):
#         return f"{self.username}"



def user_directory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to=user_directory_path)
	
	

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save()
		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
