from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

	def __str__(self):
		return f"Profile of {self.user.username}"


class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

	class Meta:
		ordering = ['-published_date']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={'pk': self.pk})
	
class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Comment by {self.author} on {self.post}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	else:
		# Ensure a profile exists and save it
		Profile.objects.get_or_create(user=instance)
		try:
			instance.profile.save()
		except Exception:
			pass