from django.db import models

# Create your models here.

from django.db import models
from datetime import datetime
from login.models import VrUser
# Create your models here.

CATEGORY_CHOICE = (
    ('Clothes',"Clothes"),
    ('Accessories','Accessories'),
    ('Books','Books'),
    ('Painting','Painting'), 
    ('Customize','Customize'),
    ('Shivaji','Shivaji'),
    ('Babasaheb','Babasaheb'),
    ('abdulkalam','abdulkalam'),
    ('bhagatsingh','bhagatsingh'),
    ('gurunanak','gurunanak'),
    ('osho','osho'),
    ('savitriphule','savitriphule'),
    ('birsamunda','birsamunda'),
    ('buddha','buddha'),
    ('santkabir','santkabir'),
    ('martinluther','martinluther'),
)

type_choice = (
    ('T-shirt','tshhirt'),
    ('Kurta','Kurta'),
    ('Mug','Mug'),
    ('Key-chain','Key-chain'),
    ('watch','watch'),
)



class product_seller(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE, default=None, null=True)
    SKUId = models.CharField(max_length=150,blank=True, null=True)
    title = models.CharField(max_length=700,blank=True, null=True)
    description = models.CharField(max_length=1000,blank=True, null=True)
    brand = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICE,max_length=50,null=True)
    product_type = models.CharField(choices=type_choice,max_length=50)
    product_image = models.ImageField(upload_to='upload_products',blank=True,null=True,default="")
    back_image = models.ImageField(upload_to='upload_products',blank=True,null=True,default="")
    left_image = models.ImageField(upload_to='upload_products',blank=True,null=True,default="")
    right_image = models.ImageField(upload_to='upload_products',blank=True,null=True,default="")
    product_video = models.FileField(upload_to='productvideos',default="",null=True,blank=True)
    product_video_url = models.URLField(max_length=200,blank=True,null=True)
    selling_price = models.FloatField(null=True, blank=True)
    discount_price = models.FloatField(null=True, blank=True, default=0.0)
    discount_type = models.CharField(max_length=100,default="",null=True,blank=True)
    actual_price = models.FloatField(default=0.0) 
    product_date=models.DateTimeField(default=datetime.now, blank=True)
    product_date1 = models.CharField(max_length=200, blank=True, null=True)
    product_approved = models.BooleanField(default=False)
    product_reject = models.BooleanField(default=False)
    quantity= models.CharField(max_length=100,default="",null=True,blank=True)
    size= models.CharField(max_length=100,default="",null=True,blank=True)
    product_id=models.CharField(max_length=100,default="",null=True,blank=True)
    sub_category=models.CharField(max_length=100,default="",null=True,blank=True)
    gender=models.CharField(max_length=100,default="",null=True,blank=True)
    product_instruction=models.CharField(max_length=500,default="",null=True,blank=True)
    manufacturer=models.CharField(max_length=100,default="",null=True,blank=True)
    model_name=models.CharField(max_length=100,default="",null=True,blank=True)
    model_number=models.CharField(max_length=100,default="",null=True,blank=True)
    age_range_description=models.CharField(max_length=100,default="",null=True,blank=True)
    bullet_point=models.CharField(max_length=1000,default="",null=True,blank=True)
    special_feature=models.CharField(max_length=2000,default="",null=True,blank=True)
    material_type=models.CharField(max_length=100,default="",null=True,blank=True)
    manufacturer_contact=models.CharField(max_length=100,default="",null=True,blank=True)
    colour=models.CharField(max_length=100,default="",null=True,blank=True)

    prod_id = models.CharField(max_length=10,null=True, blank=True)

    image_src=models.ImageField(upload_to='customize',blank=True,null=True,default="")
    tshirt_size=models.CharField(max_length=250, default=None, null=True, blank=True)
    jsonfiles=models.FileField(upload_to='json_files', blank=True, null=True, default=None)
    t_shirt_color=models.CharField(max_length=250, default=None, null=True, blank=True)
    tshirt_owndesign_s=models.ImageField(upload_to='customize',blank=True,null=True,default="")

    product_story=models.TextField(max_length=500,default='',blank=True, null=True)
    average_rating=models.CharField(max_length=10,default="",null=True,blank=True)
    discount_percentage = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return f"{self.prod_id}-{self.product_id}-{self.size}-{self.title}-{self.selling_price}"



class Commission(models.Model):
        commission_email= models.EmailField(max_length=255)
        seller_name = models.CharField(max_length=255)
        commission_plan = models.CharField(max_length=20, choices=[('zero', 'Zero Commission'), ('subscription', 'Subscription'), ('standard', 'Standard')])
        product_category = models.CharField(max_length=50, choices=CATEGORY_CHOICE, blank=True, null=True)
        product_commission_percent = models.CharField(blank=True, null=True,max_length=50)
        commission_type = models.CharField(max_length=20, choices=[('annually', 'Annually'), ('monthly', 'Monthly')], blank=True, null=True)
        product_commission_rupees = models.CharField(blank=True, null=True,max_length=50)
        commission_approved = models.BooleanField(default=False)
        commission_reject = models.BooleanField(default=False)

        STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        )
        
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='')
        approved_by = models.ForeignKey(VrUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_commissions')
        rejected_by = models.ForeignKey(VrUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_commissions')


        def __str__(self):
            return f"{self.seller_name} - {self.commission_plan}"
