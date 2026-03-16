from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from petstagram import settings

UserModel = get_user_model()

@receiver(post_save, sender=UserModel) # When we have a save on the User Model
def create_profile(sender: UserModel, instance: UserModel, created: bool, **kwargs: dict) -> None:
    if created:
        Profile.objects.create(pk=instance.pk)
        send_mail(
            subject='New account created',
            message='Welcome! Now you have a new profile!',
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[instance.email], # User Email recieves this email
            fail_silently=False,
        )