from django.db import models

# Create your models here.


class LoginProfile(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    image_type = models.CharField(max_length=50, blank=True)  # image/png, image/jpeg
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class SkillsMaster(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.TextField(blank=True, null=True)  # Base64 image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    icon = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    mindmap = models.JSONField(default=list, blank=True)  # Stores mindmap nodes as JSON

    def __str__(self):
        return self.title


class Profile(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)

    ug_degree = models.CharField(max_length=150)
    ug_university = models.CharField(max_length=200)
    ug_years = models.CharField(max_length=50)

    pg_degree = models.CharField(max_length=150, blank=True)
    pg_university = models.CharField(max_length=200, blank=True)
    pg_years = models.CharField(max_length=50, blank=True)

    photo = models.BinaryField(null=True, blank=True)

    def photo_base64(self):
        if self.photo:
            import base64
            return "data:image/jpeg;base64," + base64.b64encode(self.photo).decode()
        return None


class HireRequest(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    email = models.EmailField()

    message = models.TextField(blank=True, null=True)

    document = models.BinaryField(blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class ProjectRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    project_title = models.CharField(max_length=200)

    requirement = models.TextField()

    document = models.BinaryField(blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title