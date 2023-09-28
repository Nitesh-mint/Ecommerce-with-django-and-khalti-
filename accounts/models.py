from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        
        user = self.model(
            email = self.normalize_email(email), #normalize le capital ma cha email bhane lower case ma change garcha
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.is_active = True
        user.set_password(password) #python's built in method as pass cannot be stored in plain text
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name= last_name,
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        
        user.save(using=self._db)
        return user
    
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email  = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    #required 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email' #this is to make email default login method
    REQUIRED_FIELDS = ['first_name','last_name','username']

    def __str__(self):
        return self.email
    
    objects = MyAccountManager() #informing this class about the above class

    #this is for superadmin and admin roles
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, blank=True)
    area = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    address = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.user.first_name
    
class DeliveryAddress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=250, blank=True)
    area = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.first_name + " [" +  self.state + " " + self.area + "]"