from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)




class UserManager(BaseUserManager):
    def create_user(self, email,user_name,date_of_birth,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            #company_name=company_name,
            date_of_birth=date_of_birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,user_name,date_of_birth, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            user_name=user_name,
            date_of_birth=date_of_birth,
            password=password
            #company_name=company_name
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,user_name,date_of_birth ,password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            user_name=user_name,
            password=password,
            #comapny_name=comapny_name,
            date_of_birth=date_of_birth

        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Company(models.Model):
    company_name = models.CharField(max_length=250,blank=False)
    def __str__(self):
        return self.company_name



class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    user_name = models.CharField(null=False,max_length=255)
    date_of_birth = models.DateField(null=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.


    objects = UserManager()



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','date_of_birth','company'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
