from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class Dimensions(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dimensions"


class Categories(models.Model):
    name = models.CharField(max_length=50)
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"


class Questions(models.Model):
    ans_type_choice = [
        ('Radiobutton', 'Radiobutton'),
        ('Textbox', 'Textbox'),
        ('Upload', 'Upload'),
        ('Checkbox', 'Checkbox')
    ]

    parameter = models.CharField(max_length=50)
    question = models.CharField(max_length=500)
    enablement_dependency = models.CharField(max_length=50)
    weightage = models.CharField(max_length=10)
    ans_type = models.CharField(max_length=50, choices=ans_type_choice, default='Radiobutton')
    options = models.CharField(max_length=10000, default='')
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Org(models.Model):
    org = models.CharField(max_length=50)
    poc_name = models.CharField(max_length=50)
    poc_email = models.CharField(max_length=50)
    poc_role = models.CharField(max_length=50)

    def __str__(self):
        return self.org


class Project(models.Model):
    project = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    leader = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)

    def __str__(self):
        return self.project

class ProjectOrgChoices(models.Model):
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    response = models.TextField()

    def __str__(self):
        return self.response


class UserInfo(models.Model):
    role_choice = [
        ('admin', 'QE Admin'),
        ('user', 'QE User'),
        ('tester', 'QE Tester')
    ]
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    project = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=role_choice, default='QE Admin')
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    password_change_required = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname


class UserCategories(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    response = models.TextField()

    def __str__(self):
        return 'User id: ' + str(self.user_id.id)


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


class UserResponse(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    response = models.TextField()

    def __str__(self):
        return f'user: {self.user_id} id: {self.user_id.id}'


class InitiativeTraceability(models.Model):
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    initiatives = models.TextField()


class InitiativeDetail(models.Model):
    initiative_id = models.CharField(max_length=20)
    initiative = models.TextField()
    description = models.TextField()
    tieback = models.TextField()
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.initiative_id


class FinalInitiatives(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return f'Initiatives Data for {self.user_id}'


class UploadedFile(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    file = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.user_id} - {self.file}'
