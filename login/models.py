from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager
from django.db import models
from django.contrib.auth.models import Group,Permission
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password, **extra_fields)

class VrUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=240, unique=True) 
    first_name = models.CharField(max_length=240, blank=True, null=True)
    last_name = models.CharField(max_length=240, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    mobile_number = models.CharField(max_length=240, unique=True, blank=True, null=True)
    is_Vruser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    company_address=models.CharField(max_length=50, blank=True, null=True)
    company_name=models.CharField(max_length=50, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    google_access_token = models.TextField(blank=True, null=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'mobile_number']

    class Meta:
        verbose_name = 'VrUsers'

    def __str__(self):
        return self.email

class VrUserGroup(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class VrUserPermission(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    
    
STATE_CHOICES=(
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh ","Arunachal Pradesh "),
    ("Assam","Assam"),("Bihar","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),
    ("Jammu and Kashmir ","Jammu and Kashmir "),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Odisha","Odisha"),
    ("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),
    ("Telangana","Telangana"),
    ("Tripura","Tripura"),
    ("Uttar Pradesh","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),
    ("West Bengal","West Bengal"),
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Chandigarh","Chandigarh"),
    ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
    ("Daman and Diu","Daman and Diu"),
    ("Lakshadweep","Lakshadweep"),
    ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
    ("Puducherry","Puducherry")
)

class customer_user(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, default=None, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, default=None, null=True, blank=True)
    locality = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    pincode = models.IntegerField(null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=5000)
    is_customer = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    def __str__(self):
        return str(self.email)
    
    
class seller_user(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, default=None, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, default=None, null=True, blank=True)
    locality = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    pincode = models.IntegerField(null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=5000)
    company_address=models.CharField(max_length=50, blank=True, null=True)
    company_name=models.CharField(max_length=50, blank=True, null=True)
    is_seller = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    pan_card = models.ImageField(upload_to='pan_cards/', null=True, blank=True)
    aadhar_card = models.ImageField(upload_to='aadhar_cards/', null=True, blank=True)
    gst_document = models.ImageField(upload_to='gst_documents/', null=True, blank=True)
    
    commision = models.CharField(max_length=240, blank=True, null=True)
    seller_reject = models.BooleanField(default=False)
    seller_approved = models.BooleanField(default=False)


    
    def __str__(self):
        return str(self.email)



class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    comment = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class SubscribedEmail(models.Model):
    email = models.EmailField(unique=True)  # Assuming you want each email to be unique
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class StoreSettings(models.Model):
    store_name = models.CharField(max_length=100,null=True,blank=True)
    store_logo = models.ImageField(upload_to='store_logo/',null=True,blank=True)
    store_email = models.EmailField()
    store_contact_number = models.CharField(max_length=15,null=True,blank=True)
    store_address = models.CharField(max_length=50,null=True,blank=True)
    store_description = models.TextField(max_length=100,null=True,blank=True)
    store_city = models.CharField(max_length=50,null=True,blank=True)
    store_state = models.CharField(max_length=50,null=True,blank=True)
    store_pincode = models.CharField(max_length=20,null=True,blank=True)
    pan_no = models.CharField(max_length=20,null=True,blank=True)
    gst_no = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.store_email
    

