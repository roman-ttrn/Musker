from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class User(AbstractUser):
#     date_modified = models.DateTimeField(auto_now=True) redeclaring model User

class Meep(models.Model):
    user = models.ForeignKey(
        User, related_name="meeps", 
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=400)
    created = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="meep_like", blank=True)

    def num_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user}",
            f"{self.created}"
        )

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete = models.CASCADE
    )
    follows = models.ManyToManyField(
        'self', related_name='followed_by', 
        symmetrical=False,                      
        blank=True                                   
        )    
    date_modified = models.DateTimeField(auto_now=True)
    prof_image = models.ImageField(default='images/default.png', upload_to='images/')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): 
    if created:
        prof = Profile(user=instance)
        prof.save()
         # == prof.followers.set([Profile.objects.get(id=instance.profile.id)])

#post_save.connect(create_profile, sender=User) or decorator

