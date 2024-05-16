from django.shortcuts import render,get_object_or_404
from login.models import *
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from tablib import Dataset
from customer.models import *
from datetime import datetime
from sweetify import sweetify
import random
import string
from .models import product_seller
from Admin.models import *
# from .forms import ExcelUploadForm
# Create your views here.

def seller_base(request):
    return render(request, "seller_base.html")



from django.shortcuts import render, redirect
from .models import product_seller
#from .forms import SellerAddProductForm  # Create a Django form for your model
@login_required(login_url='/seller_login/')
def seller_add_product(request):
    if request.method == 'POST':
        characters_upper = string.ascii_uppercase 
        characters_digits = string.digits

        if 'myfile' in request.FILES:
            dataset = Dataset()
            new_persons = request.FILES['myfile']
            imported_data = dataset.load(new_persons.read(), format='xlsx')

            print("Imported Data:", imported_data)  # Print to check the structure of imported_data

            for data in imported_data:
                first_three_chars = 'PROD'
                remaining_digits = ''.join(random.choices(characters_digits, k=7))
                prod_id = f'{first_three_chars}{remaining_digits}'

                SKUId = data[0]

                # Determine discount calculation based on discount_type
                discount_type = data[11]  # Assuming discount_type is at index 11 in your data

                if discount_type == 'Rupees':
                    # Calculate discounted price in case of Rupees
                    discount_price = float(data[12])
                    selling_price = float(data[10]) - discount_price
                elif discount_type == 'Percent':
                    # Convert percentage discount to actual amount
                    discount_price = float(data[12])
                    dis_price = (float(data[12]) / 100) * float(data[10])
                    selling_price = float(data[10]) - dis_price
                else:
                    # Handle other cases or set a default value
                    discount_price = 0.0
                    selling_price = float(data[10])

                new_book = product_seller(
                    user=request.user,
                    SKUId=SKUId,
                    brand=data[1],
                    product_id=data[2],
                    size=data[3],
                    colour=data[4],
                    title=data[5],
                    description=data[6],
                    product_type=data[7],
                    category=data[8],
                    sub_category=data[9],
                    actual_price=float(data[10]),
                    discount_type=discount_type,
                    discount_price=discount_price,
                    selling_price=selling_price,
                    quantity=int(data[13]),  # Assuming quantity is an integer field
                    gender=data[14],
                    product_instruction=data[15],
                    manufacturer=data[16],
                    model_name=data[17],
                    model_number=data[18],
                    age_range_description=data[19],
                    bullet_point=data[20],
                    special_feature=data[21],
                    material_type=data[22],
                    manufacturer_contact=data[23],
                    prod_id=prod_id,
                )

                # Save the new book entry
                new_book.save()

    return render(request, 'product/seller_add_product.html')



from django.dispatch import receiver
from django.db.models.signals import pre_delete

@receiver(pre_delete, sender=VrUser)
def delete_user_files(sender, instance, **kwargs):
    # Delete associated Seller_product files
    seller_products = product_seller.objects.filter(user=instance)
    for product in seller_products:
        # Delete images
        if product.product_image:
            product.product_image.delete(save=False)
        if product.back_image:
            product.back_image.delete(save=False)
        if product.left_image:
            product.left_image.delete(save=False)
        if product.right_image:
            product.right_image.delete(save=False)
        
        # Delete video file
        if product.product_video:
            product.product_video.delete(save=False)

    # Additional cleanup if needed
    # ...

# Connect the signal
pre_delete.connect(delete_user_files, sender=VrUser)



from django.db.models import Q
def admin_approved_products(request):
    products = product_seller.objects.filter(user=request.user,product_approved=True)
    print('ooooooooooooooooooooo',products)
    return render(request,'product/admin_approved_products.html',{'products':products})


def seller_all_products(request):
    user = request.user
    data = product_seller.objects.filter(user=user)
    return render(request,'product/seller_all_products.html',{'data':data})



def seller_commission_form(request):
    seller_name = request.user.first_name + ' ' + request.user.last_name
    existing_commissions = Commission.objects.filter(seller_name=seller_name)

    if request.method == 'POST':
        commission_plan = request.POST.get('commission_plan')
        commission_email = request.POST.get('commission_email')
        product_commission_percent = request.POST.get('product_commission_percent')
        product_category = request.POST.get('product_category')
        commission_type = request.POST.get('commission_type')
        product_commission_rupees = request.POST.get('product_commission_rupees')

        for existing_commission in existing_commissions:
            existing_commission.commission_plan = commission_plan
            existing_commission.commission_email = commission_email
            existing_commission.product_commission_percent = product_commission_percent
            existing_commission.product_category = product_category
            existing_commission.commission_type = commission_type
            existing_commission.product_commission_rupees = product_commission_rupees
            existing_commission.status = "Pending"  # Assuming you need to set the status to "Pending" on update
            existing_commission.save()
            # messages.success(request, 'Commission data updated successfully! Wait for admin\'s approval.')
            # Assuming you want to update all existing commissions for the seller

        if not existing_commissions:
            new_commission = Commission(
                commission_plan=commission_plan,
                commission_email=commission_email,
                product_commission_percent=product_commission_percent,
                product_category=product_category,
                commission_type=commission_type,
                product_commission_rupees=product_commission_rupees,
                seller_name=seller_name,
                status="Pending"
            )
            new_commission.save()
            print(new_commission)
            # messages.success(request, 'New commission data saved successfully! Wait for admin\'s approval.')

        return redirect('seller_commission_form')

    data1 = Commission.objects.all()

    commi = None

    print('dddddddddddddddddddd',request.user)
    dddd = Commission.objects.filter(commission_email=request.user)
    print('dddddddddddddddddddddddddddddddddddddddddddddd',dddd)

    if dddd:
        commi = Commission.objects.get(commission_email=request.user)
        print('44444444444444',commi)

    return render(request, 'seller/commission.html', context=({'data1': data1, 'existing_commissions': existing_commissions,'commi':commi}))

def seller_view_invoice(request):
    user = request.user
    view_invoice = OrderPlaced.objects.filter(user=user)
    return render(request,'product/seller_view_invoice.html',{'view_invoice':view_invoice})


def update_product(request, product_id):
    product = get_object_or_404(product_seller, id=product_id)
    
    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.brand = request.POST.get('brand')
        product.category = request.POST.get('category')
        product.product_type =request.POST.get('product_type')
        product.selling_price = request.POST.get('selling_price')
        product.discount_price = request.POST.get('discount_price')
        product.discount_type = request.POST.get('discount_type')
        
        # Check if new images were uploaded
        new_product_image = request.FILES.get('new_product_image')
        new_back_image = request.FILES.get('new_back_image')
        new_left_image = request.FILES.get('new_left_image')
        new_right_image = request.FILES.get('new_right_image')
        
        if new_product_image:
            product.product_image = new_product_image
        if new_back_image:
            product.back_image = new_back_image
        if new_left_image:
            product.left_image = new_left_image
        if new_right_image:
            product.right_image = new_right_image
        
        product.save()
        return redirect('admin_approved_products')
    
    return render(request, 'product/update_product.html', {'product': product})



def delete_product(request, product_id):
    product = product_seller.objects.get(id=product_id)
    product.delete()
    
    return redirect('/admin_approved_products/') 

def preview_product(request, product_id):
    try:
        product = product_seller.objects.get(pk=product_id)
    except product_seller.DoesNotExist:
        product = None

    return render(request, 'product/seller_prod_preview.html', {'product': product})



def seller_cancel_orders(request):
    
    user = request.user
    seller = user
    print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',seller)
    
    orders = OrderPlaced.objects.filter(product__user=seller,canceled=True)
   
    return render(request,'seller/show_cancel_orders.html',{'orders':orders})


def seller_return_orders(request): 
    user = request.user
    seller = user
    order = OrderPlaced.objects.filter(product__user=seller,returned=True)
    print('fffffffffffffffffffffffffffffffff',user)
    return render(request, "seller/show_return_orders.html", {'order': order})  


def seller_all_orders(request):
    user = request.user
    seller = user  # Assuming the seller is also a user in your system

    # Retrieve orders placed for products belonging to the seller
    orders = OrderPlaced.objects.filter(product__user=seller)

    context = {
        'orders': orders
    }
    return render(request, "seller/customer_order_report.html", context)


def availability_report(request):
    seller_id = request.user.id
    products = product_seller.objects.filter(user_id=seller_id)
    
    low_quantity_products = []
    
    for product in products:
        try:
            quantity = int(product.quantity)
            if quantity < 15:
                low_quantity_products.append(product)
        except ValueError:
            # Handle cases where quantity is not a valid integer
            pass
    
    if low_quantity_products:
        send_low_quantity_email(request.user.email, low_quantity_products)
    
    return render(request, 'seller/availability_report.html', {'products': products})

from django.core.mail import send_mail

def send_low_quantity_email(recipient_email, low_quantity_products):
    subject = 'Low Quantity Alert'
    message = f'Dear Seller,\n\nThe following products have low quantities:\n\n'
    
    for product in low_quantity_products:
        message += f'{product.title} - Quantity: {product.quantity}\n'
    
    message += '\nPlease take necessary actions to replenish the stock.\n\nRegards,\nVishwa Ratna'
    
    send_mail(subject, message, 'myvishwaratna@gmail.com', [recipient_email])



def seller_order_tracking(request):
    user = request.user
    seller = user  # Assuming the seller is also a user in your system

    # Retrieve orders placed for products belonging to the seller
    orders = OrderPlaced.objects.filter(product__user=seller)

    context = {
        'orders': orders
    }
    return render(request, "seller/seller_order_tracking.html", context)

def edit_seller_import(request,id):
    
    seller = product_seller.objects.get(id=id)
    
        
    if request.method == 'POST':
            # Update the existing seller with the new data
            seller.title = request.POST.get('title')
            seller.SKUId = request.POST.get('SKUId')
            seller.brand = request.POST.get('brand')
            seller.colour = request.POST.get('colour')
            seller.category=request.POST.get("category")
            seller.product_type=request.POST.get("product_type")
            seller.sub_category=request.POST.get("sub_category")
            seller.product_id=request.POST.get("product_id")
            seller.quantity=request.POST.get("quantity")
            seller.model_name=request.POST.get("model_name")
            seller.model_number=request.POST.get("model_number")
            
            
            seller.product_image = request.FILES.get('product_image')  # Handle uploaded image file
            seller.back_image = request.FILES.get('back_image')
            seller.left_image = request.FILES.get('left_image')
            seller.right_image = request.FILES.get('right_image')
            seller.right_image = seller.right_image 
            seller.product_image=seller.product_image
            seller.back_image=seller.back_image
            seller.left_image=seller.left_image
            # Save the updated seller entry
            seller.save()
            print("77777777777777",seller,seller.product_image)
            
           
        
    
    context = {
        'seller': seller,
    }
    return render(request, 'product/edit_seller_import.html', context)



def view_order_seller(request, id):
    order_details = get_object_or_404(OrderPlaced, id=id)
    tracking_details = TrackingDetail.objects.filter(order=order_details).order_by('-date_time')

    if request.method == 'POST':
        update_location = request.POST.get('location')
        status = request.POST.get('status')
        cod = request.POST.get('cod')

        if update_location:
            if not order_details.location1:
                order_details.location1 = update_location
            elif not order_details.location2:
                order_details.location2 = update_location
            elif not order_details.location3:
                order_details.location3 = update_location
            else:
                # Handle additional locations or raise an error if necessary
                pass

        order_details.update_location = update_location
        order_details.status = status
        order_details.remark = status
        order_details.cod_amount = cod

        if status == 'Delivered':
            # If status is Delivered, update cod_amount with total_cost
            order_details.cod_amount = order_details.total_cost

        order_details.save()

        # Create a new TrackingDetail object to store the location update
        new_tracking_detail = TrackingDetail(order=order_details, location=update_location, date_time=timezone.now(), remark=status)
        new_tracking_detail.save()
        
    return render(request, 'seller/view_order_seller.html', {'order_details': order_details, 'tracking_details': tracking_details, 'STATUS_CHOICE': STATUS_CHOICE})

