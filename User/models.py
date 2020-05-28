from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from PIL import Image


ROLE = (('HM', 'HM'), ('T', 'T'), ('S', 'S'), ('P', 'P'))
# all users table which contain the mutual fields
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=50, null=False, blank=False, choices=ROLE)
    avatar = models.ImageField(upload_to=None)
    address = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(auto_now_add=True)
    # override save function to check that user avatar less than 300px so resizing it and save it
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.width > 300 or img.height > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
        pass


# class room table 
class ClassRoom(models.Model):
    uni_code = models.CharField(max_length=255, blank=False, null=False)
    number = models.CharField(max_length=10, null=False, blank=False)
    grade = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=10, null=False, blank=False)
    level = models.CharField(max_length=10, null=False, blank=False)
    # override save function to create class name like 3/1
    def save(self, *args, **kwargs): 
        self.name = '{}/{}'.format(self.number, self.grade)
        super(ClassRoom, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    grade = models.CharField(max_length=10, null=False, blank=False)
    level = models.CharField(max_length=10, null=False, blank=False)
    educational_type = models.CharField(max_length=100, null=False, blank=False)

    def set_name(self, name):
        self.name = name

class HeadMaster(models.Model):
    school_name = models.CharField(max_length=255, null=False, blank=False)
    uni_code = models.SlugField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    educational_type = models.CharField(max_length=100, null=False, blank=False)
    educational_level = models.CharField(max_length=100, null=False, blank=False)

    def set_user(self, user):
        self.user = user

    def save(self, *args, **kwargs): 
        self.uni_code = slugify(self.school_name + '-' + self.educational_type + '-' + self.educational_level)
        super(HeadMaster, self).save(*args, **kwargs)

class Teacher(models.Model):
    uni_code = models.CharField(max_length=255, blank=False, null=False)
    grade = models.CharField(max_length=10, null=False, blank=False)
    level = models.CharField(max_length=10, null=False, blank=False)
    class_rooms = models.ManyToManyField(ClassRoom , blank = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,blank = True , null=True)

    def set_user(self, user):
        self.user = user

    def set_uni_code(self, uni_code):
        self.uni_code = uni_code

    def set_subject(self, subject):
        self.subject = subject

class Parent(models.Model):
    uni_code = models.CharField(max_length=255, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def set_uni_code(self, uni_code):
        self.uni_code = uni_code

    def set_user(self, user):
        self.user = user

class Student(models.Model):
    uni_code = models.CharField(max_length=255, blank=False, null=False)
    grade = models.CharField(max_length=10, null=False, blank=False)
    level = models.CharField(max_length=10, null=False, blank=False)
    subjects = models.ManyToManyField(Subject, blank = True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,blank = True , null=True , related_name='student_class')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    # Father_Info_First_Name = models.CharField(max_length=50, null=True, blank=True)
    # Father_Info_Family_Name = models.CharField(max_length=50, null=True, blank=True)
    # Father_Info_Email = models.EmailField()
    # Father_Info_Mobile = models.CharField(max_length=50, null=True, blank=True)
    # Mother_Info_First_Name = models.CharField(max_length=50, null=True, blank=True)
    # Mother_Info_Family_Name = models.CharField(max_length=50, null=True, blank=True)
    # Mother_Info_Email = models.EmailField()
    # Mother_Info_Mobile = models.CharField(max_length=50, null=True, blank=True)

    def set_classrom(self, class_room):
        self.class_room = class_room

    def set_uni_code(self, uni_code):
        self.uni_code = uni_code

    def set_user(self, user):
        self.user = user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
