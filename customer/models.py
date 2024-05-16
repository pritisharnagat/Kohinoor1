from django.db import models

# Create your models here.
from login.models import *
from seller.models import *

class cart(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    product = models.ForeignKey(product_seller, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=100,null=True, blank=True)
    anonymous_user_id = models.CharField(max_length=100, null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    image_src = models.ImageField(upload_to='customize', null=True, blank=True,default="")
   
    def __str__(self):
        return str(self.user)          

class Wishlist(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    product = models.ForeignKey(product_seller, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)                      


class CustomerQuery(models.Model):
    customer = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject


STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed',"packed"),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)    


class OrderPlaced(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer_user, on_delete=models.CASCADE)
    product = models.ForeignKey(product_seller, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=100,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for product price
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # New field for tax
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.CharField(max_length=10,null=True, blank=True)
    Order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices = STATUS_CHOICE ,default ='Pending')
    remark = models.CharField(max_length=50, null=True, blank=True )
    #commision = models.CharField(max_length=50 ,default ='Pending')
    payment_method = models.CharField(max_length=10,null=True, blank=True)
    invoice_no = models.CharField(max_length=10,null=True, blank=True)

    canceled = models.BooleanField(default=False)
    cancel_reason = models.TextField(blank=True)
    returned = models.BooleanField(default=False)
    return_reason = models.TextField(blank=True)

    location = models.CharField(max_length=100,null=True, blank=True )
    update_location = models.CharField(max_length=100,null=True, blank=True )
    location1 = models.CharField(max_length=100, null=True)
    location2 = models.CharField(max_length=100, null=True)
    location3 = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(auto_now=True)
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    razorpay_order_id=models.CharField(max_length=100, null=True)
    razorpay_payment_id=models.CharField(max_length=100, null=True)
    
    Delivered = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(null=True, blank=True)
    product_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    image_src=models.ImageField(upload_to='customize',blank=True,null=True,default="")
    tshirt_size=models.CharField(max_length=250, default=None, null=True, blank=True)
    jsonfiles=models.FileField(upload_to='json_files', blank=True, null=True, default=None)
    t_shirt_color=models.CharField(max_length=250, default=None, null=True, blank=True)
    tshirt_owndesign_s=models.ImageField(upload_to='customize',blank=True,null=True,default="")
    selloship_id = models.CharField(max_length=10,null=True, blank=True)


    def __str__(self):
        return f"{self.user} - Invoice No: {self.invoice_no} - Order ID: {self.order_id}"


class Customer_Review(models.Model):
    product = models.ForeignKey(product_seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default=None, null=True, blank=True)
    email = models.EmailField(max_length=250, default=None, null=True, blank=True)
    review_star = models.CharField(max_length=50,null = True, blank= True,default='')
    review = models.CharField(max_length=500,default='', null = True, blank= True)
    average_rating = models.CharField(max_length=500,default='', null = True, blank= True)
    customer_image = models.ImageField(upload_to='upload_products', blank=True, null=True, default='')

    def __str__(self):
        return f"{self.product} - {self.product.title} Review"



class CanceledOrder(models.Model):
    order_id = models.CharField(max_length=100)
    customer = models.ForeignKey(customer_user, on_delete=models.CASCADE)
    product = models.ForeignKey(product_seller, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    canceled_reason = models.TextField()
    canceled_at = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=True)  # New field to indicate if order is canceled
    payment_method = models.CharField(max_length=10,null=True, blank=True)
    invoice_no = models.CharField(max_length=10,null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    razorpay_order_id=models.CharField(max_length=100, null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100, null=True,blank=True)


    def __str__(self):
        return f"CanceledOrder: {self.order_id}"  



class Customize_product(models.Model):
    user = models.ForeignKey(VrUser, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer_user, on_delete=models.CASCADE)
    image_src=models.ImageField(upload_to='customize',blank=True,null=True,default="")
    tshirt_size=models.CharField(max_length=250, default=None, null=True, blank=True)
    jsonfiles=models.FileField(upload_to='json_files', blank=True, null=True, default=None)
    t_shirt_color=models.CharField(max_length=250, default=None, null=True, blank=True)
    tshirt_owndesign_s=models.ImageField(upload_to='customize',blank=True,null=True,default="")


    def __str__(self):
        return f"Customize_product - User: {self.user}, Customer: {self.customer}"

class Customize(models.Model):
    image_src=models.ImageField(upload_to='customize',blank=True,null=True,default="")
    tshirt_size=models.CharField(max_length=250, default=None, null=True, blank=True)
    jsonfiles=models.FileField(upload_to='json_files', blank=True, null=True, default=None)
    t_shirt_color=models.CharField(max_length=250, default=None, null=True, blank=True)
    tshirt_owndesign_s=models.ImageField(upload_to='customize',blank=True,null=True,default="")


    
