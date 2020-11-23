from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _ 


class UserManager(BaseUserManager):
    def create_user(self, email, fname, lname, password=None, is_active=True, is_staff=False, is_admin=False, type='REGULAR'):
        if not email:
            raise ValueError("User must have email address")
        if not password:
            raise ValueError("User must have password")
        if not fname:
            raise ValueError("User must have name")
        user_object = self.model(
            email = self.normalize_email(email)
        )

        user_object.set_password(password)
        user_object.staff = is_staff
        user_object.admin = is_admin
        user_object.active = is_active
        user_object.fname = fname
        user_object.lname = lname
        
        user_object.save(using=self._db)

        return user_object

    def create_staffuser(self, email, fname, lname=None, password=None):
        user = self.create_user(
            email,
            fname=fname,
            lname=lname,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, fname, lname=None, password=None):
        user = self.create_user(
            email,
            fname=fname,
            lname=lname,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    def create_constractor(self, email, fname, lname=None, password=None):
        user = self.create_user(
            email,
            fname=fname,
            lname=lname,
            password=password,
            is_staff=False,
            is_admin=False,
            type='CONTRACTOR'
        )
        return user    

# Create your models here.
class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    fname       = models.CharField(_('First Name'), max_length = 255, blank=True, null=True)
    lname       = models.CharField(_('Middle Name'), max_length = 255, blank=True, null=True)
    mname       = models.CharField(_('Last Name'), max_length = 255, blank=True, null=True)
    address1    =  models.CharField(_('Address 1'), max_length = 255, blank=True, null=True)
    address2    =  models.CharField(_('Address 2'), max_length = 255, blank=True, null=True)
    city        =  models.CharField(_('City'), max_length = 255, blank=True, null=True)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    complete_info = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Types(models.TextChoices):
        REGULAR = "REGULAR", "Regular"
        COMPANY = "COMPANY", "Company"
        
    type = models.CharField(_('Type'), max_length = 50, choices=Types.choices, default= Types.REGULAR)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.fname + self.lname

    def get_short_name(self):
        return self.fname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    #def get_absolute_url(self): 
    #    return reverse("users:details", kwargs={"username": self.username})

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_regular(self):
        return self.type == 'REGULAR'

    @property
    def is_company(self):
        return self.type == 'COMPANY'
                        

class RegularManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.REGULAR)

class CompanyManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COMPANY)


class Regular(User):
    objects = RegularManager()
    class Meta:
        proxy = True


class Company(User):
    objects = CompanyManager()
    class Meta:
        proxy = True
            

