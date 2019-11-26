from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile_number, password, **extra_fields):
        """
        Create and save a user with the given phone number, and password.
        """
        if not mobile_number:
            raise ValueError('The given phone number must be set')
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, password, **extra_fields)


class SignUp(AbstractBaseUser):

    class Meta:
    	db_table = "signup"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number  = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    country_code =  models.CharField(max_length=50)
    is_admin = models.BooleanField(
        'superuser',
        default=True,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_superuser = models.BooleanField(
        'superuser',
        default=True,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active.',
    )    

    USERNAME_FIELD = 'mobile_number'
    objects = UserManager()

    def has_module_perms(self, app_label):
       return self.is_admin

    def has_perm(self, perm, obj=None):
       return self.is_admin


class UserMaster(models.Model):
	mobile_number = models.ForeignKey('SignUp', on_delete=models.CASCADE)
	profile = models.FileField(upload_to='profile', blank=True)

	class Meta:
		db_table = "usermaster"

