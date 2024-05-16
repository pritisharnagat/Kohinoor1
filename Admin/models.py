# from django.db import models

# # Create your models here.

from django.db import models
from datetime import datetime    
from django.utils import timezone
from login.models import VrUser
from django.utils import timezone
from customer.models import OrderPlaced
# # Create your models here.


CATEGORY_CHOICE = (
    ('TS',"Clothes"),
    ('AC','Accessories'),
    ('BK','Books'),
    ('PT','Painting'), 
)

type_choice = (
    ('T-shirt','T-shirt'),
    ('Kurta','Kurta'),
    ('Mug','Mug'),
    ('Key-chain','Key-chain'),
    ('watch','watch'),

    )


class Admin_Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICE,max_length=15,blank=True, null=True)
    product_type = models.CharField(choices=type_choice,max_length=50,default =None,blank=True, null=True)
    product_image = models.ImageField(upload_to='upload_products',blank=True, null=True,default="")
    back_image = models.ImageField(upload_to='upload_products', blank=True, null=True)
    left_image = models.ImageField(upload_to='upload_products', blank=True, null=True,default="")
    right_image = models.ImageField(upload_to='upload_products', blank=True, null=True,default="")
    product_video = models.FileField(upload_to='productvideos',default="", null=True, blank=True)
    product_date=models.DateTimeField(default=datetime.now, blank=True)
    product_date1 = models.CharField(max_length=200, blank=True, null=True)
    product_video_url = models.URLField(max_length=200, blank=True, null=True)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discount_type = models.CharField(max_length=100,default="", null=True, blank=True)
    actual_price = models.FloatField(default=0.0) 

    def __str__(self):
        return str(self.id)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    heading1 = models.CharField(max_length=50,null=True, blank=True)
    heading2 = models.CharField(max_length=50,null=True, blank=True)
    heading3 = models.CharField(max_length=50,null=True, blank=True)
    heading4 = models.CharField(max_length=50,null=True, blank=True)
    heading5 = models.CharField(max_length=50,null=True, blank=True)
    heading6 = models.CharField(max_length=50,null=True, blank=True)
    heading7 = models.CharField(max_length=50,null=True, blank=True)
    heading8 = models.CharField(max_length=50,null=True, blank=True)
    heading9 = models.CharField(max_length=50,null=True, blank=True)
    heading10 = models.CharField(max_length=50,null=True, blank=True)
    content1 = models.TextField(null=True, blank=True)
    content2 = models.TextField(null=True, blank=True)
    content3 = models.TextField(null=True, blank=True)
    content4 = models.TextField(null=True, blank=True)
    content5 = models.TextField(null=True, blank=True)
    content6 = models.TextField(null=True, blank=True)
    content7 = models.TextField(null=True, blank=True)
    content8 = models.TextField(null=True, blank=True)
    content9 = models.TextField(null=True, blank=True)
    content10 = models.TextField(null=True, blank=True)
    image1 = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=100,null=True, blank=True)
    blog_created_date = models.DateTimeField(default=timezone.now, blank=True)


    def __str__(self):
        return str(self.title)


class TrackingDetail(models.Model):
    order = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True)
    # status = models.CharField(max_length=100, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=50, null=True, blank=True )


    def __str__(self):
        return f"Order: {self.order.id}, Location: {self.location}, Date & Time: {self.date_time}"


class customized_Designed(models.Model):
    
    image1 = models.ImageField(upload_to='upload_products', blank=True, null=True)
    image2 = models.ImageField(upload_to='upload_products', blank=True, null=True,default="")
    image3 = models.ImageField(upload_to='upload_products', blank=True, null=True,default="")
    image4 = models.ImageField(upload_to='upload_products', blank=True, null=True,default="")
    image5 = models.ImageField(upload_to='upload_products',blank=True, null=True,default="")

    def __str__(self):
        return f"Designed: {self.id}"  


class emailSetting(models.Model):
    email_type = models.CharField(max_length=100, null=True)
    smtp_username = models.CharField(max_length=100, null=True)
    smtp_password = models.CharField(max_length=100, null=True)
    smtp_server = models.CharField(max_length=100, null=True)
    smtp_port = models.CharField(max_length=100, null=True)
    smtp_security = models.CharField(max_length=100, null=True)


class about_us(models.Model):
    history = models.TextField(null=True,blank=True,default='')
    vision = models.TextField(null=True,blank=True,default='')
    mission = models.TextField(null=True,blank=True,default='')

class faqs(models.Model):
    question = models.CharField(max_length=100, null=True,blank=True,default='')
    answers =  models.TextField(null=True,blank=True,default='')
    
class Event(models.Model):
    event_date = models.DateField()
    event_name = models.CharField(max_length=200, blank=True, null=True)   
    event_discount = models.FloatField(default=0.0)
    
    def __str__(self):
        return str(self.event_name)

class RazorpaySettings(models.Model):
    razorpay_key_id = models.CharField(max_length=100,blank=True, null=True)
    rezorpay_key_secret = models.CharField(max_length=100,blank=True, null=True)
    
    def __str__(self):
        return f'RazorpaySettings'

class Collections_Thought(models.Model):
    subcategory=models.CharField(max_length=100,default="",null=True,blank=True)
    heading = models.CharField(max_length=100,null=True, blank=True)
    heading1 = models.CharField(max_length=100,null=True, blank=True)
    heading2 = models.CharField(max_length=100,null=True, blank=True)
    heading3 = models.CharField(max_length=100,null=True, blank=True)
    heading4 = models.CharField(max_length=100,null=True, blank=True)
    heading5 = models.CharField(max_length=100,null=True, blank=True)
    heading6 = models.CharField(max_length=100,null=True, blank=True)
    paragraph1 = models.CharField(max_length=500,null=True, blank=True)
    paragraph2 = models.CharField(max_length=500,null=True, blank=True)
    paragraph3 = models.CharField(max_length=500,null=True, blank=True)
    paragraph4 = models.CharField(max_length=500,null=True, blank=True)
    paragraph5 = models.CharField(max_length=500,null=True, blank=True)
    paragraph6 = models.CharField(max_length=500,null=True, blank=True)
    paragraph7 = models.CharField(max_length=500,null=True, blank=True)