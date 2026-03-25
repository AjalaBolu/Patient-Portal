from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Automatically create or update Profile whenever a User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    from .models import Profile
    # Only create profiles for non-staff (patients)
    if not instance.is_staff and not instance.is_superuser:
        if created:
            Profile.objects.create(user=instance)
        else:
            # Safely update if profile exists
            if hasattr(instance, "profile"):
                instance.profile.save()
