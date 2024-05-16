from django.shortcuts import render,redirect,get_object_or_404
from .models import * 
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
# def bootstrap_cus(request):
#     return render(request, "customer_base.html")

from django.db.models import Count
from django.db.models import Avg
import string
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render
from Admin.models import *
from django.shortcuts import render, redirect
from .models import OrderPlaced
from django.http import HttpResponseBadRequest
from django.db.models import F
from decimal import Decimal
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from Admin.models import *

def view_cart(request):
    user = request.user.username
    cart_items = cart.objects.filter(user__username=user).order_by('-id')

    total_amount = 0.0
    for item in cart_items:
        total_amount += item.quantity * item.product.actual_price
        total_amount = round(total_amount, 2)

    return render(request,'customer/cart.html',{'cart_items':cart_items,'total_amount':total_amount})
    
@login_required(login_url='/customer_login/')
def remove_cart(request,id):
    if request.method == 'GET':
        user = request.user
        c = cart.objects.get(id=id,user=user)
        c.delete()

    return redirect("/view_cart/")   

@login_required(login_url='/customer_login/')
def add_wishlist(request):
    if request.method == 'POST':
        user = request.user
        prod_id  = request.POST.get('prod_id')
        # print(f"Product IDDDDDDDDDDDDDDDDDDDDDDDD: {prod_id}")
        product = product_seller.objects.get(prod_id=prod_id)
        wishlist = Wishlist(user=user, product=product)
        wishlist.save()
        return redirect("/view_wishlist/".format(prod_id))
    


@login_required(login_url='/customer_login/')  
def view_wishlist(request):
    if request.user.is_authenticated:
        user = request.user.username
        data = Wishlist.objects.filter(user__username = user).order_by('-id')
        
        count = data.count()
        
        context={
            'data':data,
            'count':count,
        }
        return render(request,'customer/wishlist.html',context)
    else:
        return redirect("/customer_login/")
    

def remove_wishlist(request,id):
    if request.method == 'GET':
        user = request.user
        w = Wishlist.objects.get(id=id,user=user)
        w.delete()

    return redirect("/view_wishlist/")   


def prod_details(request, prod_id):
    # data=product_seller.objects.filter(product_type="tshhirt").order_by('-id')[:4]
    product = product_seller.objects.get(prod_id=prod_id)

    product_type = product.sub_category
    related_products = product_seller.objects.filter(sub_category=product_type).order_by('-id')[:4]

    # Get products with the same type as the specified product
    similar_products = product_seller.objects.filter(product_type=product.product_type,title=product.title)
    product_colors = {}
    product_images = {}
    product_size = {}
    print('aparnadddddddddddd',similar_products)
    # Extract color variations for each similar product

    # Colors aur images ko collect karna
    for similar_product in similar_products:
        colors = product_seller.objects.filter(product_type=similar_product.product_type, title=similar_product.title).values_list('colour', flat=True)
        size = product_seller.objects.filter(product_type=similar_product.product_type, title=similar_product.title).values_list('size', flat=True)

        product_colors[similar_product] = list(colors)
        product_size[similar_product] = list(size)
        image_url = similar_product.product_image.url if similar_product.product_image else None
        for color in colors:
            product_images[color] = image_url

    # Available colors ko collect karna
    available_colors = list(product_colors.keys())
    

    if request.method == 'POST':
        selected_color = request.POST.get('color')

        # Selected color ke corresponding t-shirt ka image URL retrieve karna
        tshirt_image_url = product_images.get(selected_color)
        # Code for handling reviews and ratings
        name = request.POST.get('name')
        review_star = request.POST.get('review_star')
        review = request.POST.get('review')
        
        new_review = Customer_Review(product_id=prod_id, name=name, review_star=review_star, review=review)
        new_review.save()

        reviews = Customer_Review.objects.filter(product_id=prod_id)

        product_ratings = Customer_Review.objects.filter(product_id=prod_id).aggregate(Avg('review_star'))['review_star__avg']
        average_rating = round(product_ratings) if product_ratings is not None else 0

        star_counts = reviews.values('review_star').annotate(count=Count('review_star'))
        total_reviews = reviews.count()
        star_ratings = {}

        for star_count in star_counts:
            star_value = star_count['review_star']
            count = star_count['count']
            percentage = round((count / total_reviews) * 100)
            star_ratings[star_value] = percentage


        context = {
            'available_colors': available_colors,
            'tshirt_image_url': tshirt_image_url,
            'average_rating': average_rating,
            'reviews': reviews,
            'star_ratings': star_ratings,
            'data':related_products
        }

        return render(request, 'product/prod_details.html', context)
    else:
        context = {
            'available_colors': available_colors,
            'product': product,
            'product_colors': product_colors,
            'prod_id':prod_id,
            'data':related_products,
            'product_size': product_size,
           
        }
        return render(request, 'product/prod_details.html', context)





from customer.models import *
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required(login_url='/customer_login/')
def checkout_view(request):
    user = request.user
    add = customer_user.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    cart_items_count = cart_items.count()
    amount = 0.0
    shipping_amount = 50
    total_amount = 0.0
    mrp_amount = 0.0
    discount_on_mrp = 0.0
    tax = 0.0
    ship = 50  # Shipping cost
    grand_total = 0.0
    
    cart_product = [p for p in cart_items if p.user == request.user]
    
    if cart_product:
        for p in cart_product:
            mrp_temp_amount = p.quantity * p.product.selling_price
           
            mrp_amount += mrp_temp_amount
           
            total_amount = mrp_amount + shipping_amount

        tax = (mrp_amount * 18) / 100  # 18% tax
        
        grand_total = tax  + total_amount
        

    pay = request.POST.get('flexRadioDefault')
    

    currency = 'INR'
    amount = grand_total*100 # Rs. 200
    print('amamamamam',amount)


    # we need to pass these details to frontend.
    context = {'mrp_amount': mrp_amount, 'cart_items_count': cart_items_count,
               'add': add, 'cart_items': cart_items, 'amount': amount,
               'total_cost': total_amount, 'discount_on_mrp': discount_on_mrp,
               'tax': tax, 'ship': ship, 'grand_total': grand_total}

    return render(request, 'customer/checkout.html', context=context)


from decimal import Decimal
def payment_method(request):
    custid = request.GET.get('custid')
    print("222222222222222222222222222222222222222",custid)
    user = request.user
    print("111111111111111111111111111111111111111111111111111",user)
    cust = customer_user.objects.get(id=custid)
    cart_items = cart.objects.filter(user=cust.user)

    for cart_item in cart_items:
        product = cart_item.product

        if int(product.quantity) <= 0:
            return HttpResponseBadRequest("One or more products in your cart are not available.")

        # Update the price field based on the product's discount price
        price = Decimal(product.discount_price)
    mrpamount = sum(Decimal(p.quantity) * Decimal(p.product.selling_price) for p in cart_items)
    tax = (mrpamount * Decimal('0.18'))
    ship = Decimal('50')
    totalamount = mrpamount + tax + ship
    grand_total = totalamount
    print("33333333333333333333333333333333333333333",cust)
    currency = 'INR'
    amount =  float(grand_total * 100)
    print('amamamamam',amount)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))
    
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    
    # callback_url = 'https://127.0.0.1:8000/paymenthandler/'
    callback_url = f'https://vishwaratna.in/paymenthandler/?custid={custid}'

    context = {
        'amount':amount,
        'cust': cust,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price,
        'grand_total': grand_total,
        'totalamount': totalamount,
        'custid':custid,
    }
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url


    return render(request,'customer/checkout_payment.html',context)


@csrf_exempt
def paymenthandler(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=('rzp_test_KbL0swDqOzzJJF', '1TmuVSs82K2NQkAaP3mHmOyA'))
        return client.utility.verify_payment_signature(response_data)

    if request.method == 'POST':
        # try:
            payment_id = request.POST.get("razorpay_payment_id", "")
            print("999999999999999999999999999999999999999999999999999999",payment_id)
            provider_order_id = request.POST.get("razorpay_order_id", "")
            custid = request.GET.get('custid')
            user = request.user

            pay = 'Razorpay'
            cust = customer_user.objects.get(id=custid)
            
            cart_items = cart.objects.filter(user=cust.user)

            characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
            order_id = ''.join(random.choices(characters, k=6))

            characters_upper = string.ascii_uppercase 
            characters_digits = string.digits  
            first_three_chars = ''.join(random.choices(characters_upper, k=3))
            remaining_digits = ''.join(random.choices(characters_digits, k=7))
            invoice_id = f'{first_three_chars}{remaining_digits}'
            
            # Generate order and invoice IDs
            characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
            order_id = ''.join(random.choices(characters, k=6))
            characters_upper = string.ascii_uppercase 
            characters_digits = string.digits  
            first_three_chars = ''.join(random.choices(characters_upper, k=3))
            remaining_digits = ''.join(random.choices(characters_digits, k=7))
            invoice_id = f'{first_three_chars}{remaining_digits}'
            
            # Process each item in the cart and create orders
            for cart_item in cart_items:
                product = cart_item.product

                if int(product.quantity) <= 0:
                    return HttpResponseBadRequest("One or more products in your cart are not available.")

                # Update the price field based on the product's discount price
                price = Decimal(product.discount_price)
                
                # Update product quantity and delete cart item
                product.quantity = int(product.quantity) - cart_item.quantity
                product.save()  
                cart_item.delete()

                # Create order
                order = OrderPlaced.objects.create(
                    user=user,
                    customer=cust,
                    product=product,
                    quantity=cart_item.quantity,
                    size=cart_item.size,
                    price=price,
                    order_id=order_id,
                    payment_method=pay,
                    invoice_no=invoice_id,
                    razorpay_order_id=provider_order_id,
                    razorpay_payment_id=payment_id
                )

            # Calculate total price of all items in the cart
            mrpamount = sum(Decimal(p.quantity) * Decimal(p.product.selling_price) for p in cart_items)
            tax = (mrpamount * Decimal('0.18'))
            ship = Decimal('50')
            totalamount = mrpamount + tax + ship
            grand_total = totalamount
            
            # Update order details with total cost
            data = OrderPlaced.objects.filter(user=user, order_id=order_id)
            for item in data:
                item.tax = tax
                item.total_cost = grand_total
                item.save()

    context = {
        'grand_total': grand_total,
        'tax': tax,
        'totalamount': totalamount,
        'data': data,
        'cust': cust,
        'order_id': order_id,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price
    }
    return render(request, "customer/order_success.html", context)



def add_to_cart(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'add_to_cart':
            user = request.user
            prod_id = request.POST.get('prod_id')
            product = product_seller.objects.get(prod_id=prod_id)
            quantity = request.POST.get('quantity', 1)  # Default quantity is 1
            size = request.POST.get('size')
            
            existing_cart_item = None
            if user.is_authenticated:
                existing_cart_item = cart.objects.filter(user=user, product=product).first()
            else:
                anonymous_user_id = request.session.session_key
                if anonymous_user_id:
                    existing_cart_item = cart.objects.filter(anonymous_user_id=anonymous_user_id, product=product).first()
                    
            if existing_cart_item:
                messages.error(request, f'The product is already in your cart.')
            else:
                try:
                    if user.is_authenticated:
                        cart(user=user, product=product, quantity=quantity, size=size).save()
                    else:
                        if not anonymous_user_id:
                            request.session.save()
                            anonymous_user_id = request.session.session_key
                        cart(anonymous_user_id=anonymous_user_id, product=product, quantity=quantity, size=size).save()
                except IntegrityError:
                    messages.error(request, "An error occurred while adding the product to your cart.")
                
            return redirect('/view_cart/')
        
        elif request.POST.get('action') == 'buy_now':
            user = request.user
            prod_id = request.POST.get('prod_id')
            product = product_seller.objects.get(prod_id=prod_id)
            quantity = request.POST.get('quantity', 1)  # Default quantity is 1
            size = request.POST.get('size')

            if user.is_authenticated:
                user_cart_items = cart.objects.filter(user=user)
                user_cart_items.delete()  # Clear existing cart items for the authenticated user
                cart(user=user, product=product, quantity=quantity, size=size).save()
                return redirect('/checkout/')
            else:
                anonymous_user = request.session.session_key
                if not anonymous_user:
                    request.session.save()
                    anonymous_user = request.session.session_key

                try:
                    cart(anonymous_user_id=anonymous_user, product=product, quantity=quantity, size=size).save()
                except IntegrityError:
                    messages.error(request, "An error occurred while adding the product to your cart.")
                    
                request.session['anonymous_user'] = anonymous_user
                return redirect('/customer_login/')
                
    return redirect('/prod_details/{prod_id}/')

def save_address1(request):
    if request.method == 'POST':
        # Extract data from the POST request
        first_name = request.POST.get('fname')
        mobile_number = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        print('ooooooooooooooooooooooooooo',first_name,mobile_number,email,locality,city,state,pincode)
        # Create a new Customer object and save it to the database
        customer = customer_user(
            user=request.user,  # Assuming you have a logged-in user
            first_name=first_name,
            email=email,
            mobile_number=mobile_number,
            locality=locality,
            city=city,
            state=state,
            pincode=pincode)
        
        customer.save()
    return redirect('/checkout/')



@login_required(login_url='/customer_login/')
def create_order(request):
    custid = request.GET.get('custid')
    user = request.user
    pay = request.GET.get('flexRadioDefault')
    cust = customer_user.objects.get(id=custid)
    
    cart_items = cart.objects.filter(user=cust.user)
    
    characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
    order_id = ''.join(random.choices(characters, k=6))

    characters_upper = string.ascii_uppercase 
    characters_digits = string.digits  
    first_three_chars = ''.join(random.choices(characters_upper, k=3))
    remaining_digits = ''.join(random.choices(characters_digits, k=7))
    invoice_id = f'{first_three_chars}{remaining_digits}'
    
    for cart_item in cart_items:
        product = cart_item.product

        if int(product.quantity) <= 0:
            return HttpResponseBadRequest("One or more products in your cart are not available.")

        # Update the price field based on the product's discount price
        price = Decimal(product.discount_price)
        
        order = OrderPlaced.objects.create(
            user=user,
            customer=cust,
            product=product,
            quantity=cart_item.quantity,
            size=cart_item.size,
            price=price,  # Use discount price for online payment
            order_id=order_id,
            payment_method=pay,
            invoice_no=invoice_id
        )

        product.quantity = F('quantity') - cart_item.quantity
        product.save()  
        cart_item.delete()

    data = OrderPlaced.objects.filter(user=user, order_id=order_id)
   # Calculate total price of all items in the cart
    mrpamount = sum(Decimal(p.quantity) * Decimal(p.product.selling_price) for p in cart_items)
    tax = (mrpamount * Decimal('0.18'))
    ship = Decimal('50')
    totalamount = mrpamount + tax + ship
    grand_total = totalamount
    
    for item in data:
        item.tax = tax
        item.total_cost = grand_total
        item.save()

    subject = 'Your Order Has Been Placed Successfully'
    from_email = 'mailto:zappkodesolutions@gmail.com'  # Replace with your email
    recipient_list = [cust.user.email]

    email_context = {
        'order_items': data,
        'order_total': totalamount,
        'order_tax': tax,
        'order_shipping': ship,
        'order_grand_total': grand_total,
    }

    context = {
        'grand_total': grand_total,
        'tax': tax,
        'totalamount': totalamount,
        'data': data,
        'cust': cust,
        'order_id': order_id,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price
    }
    
    return render(request, "customer/order_success.html", context)



def invoice(request, order_id):
    user = request.user

    # Assuming you have a tax rate, replace 0.1 with your actual tax rate
    
    order = OrderPlaced.objects.filter(user=user, order_id=order_id)
   

   
   
    return render(request, "customer/invoice.html", {'order': order})





@login_required
def add_queries(request):

    customer = request.user
    query_answered = CustomerQuery.objects.filter(customer=customer)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject and message:
            query = CustomerQuery.objects.create(
                customer=request.user,
                subject=subject,
                message=message,
                timestamp=timezone.now()
            )

    
    
    return render(request, 'customer/add_queries.html',{'query_answered':query_answered})



def return_order(request, order_id):
    order = OrderPlaced.objects.get(order_id=order_id)
    if request.method == 'POST':
        return_reason = request.POST.get('return_reason')
        order.returned = True
        order.return_reason = return_reason 
        order.save()
        
        order_items = OrderPlaced.objects.filter(order_id=order_id)
        for item in order_items:
            product = item.product
            quantity_ordered = item.quantity
            product.quantity = F('quantity') + quantity_ordered
            product.save()
            
        return redirect('/orders/')  
    return render(request, 'customer/return_orders.html', {'order': order})
    

def customization(request,prod_id):
    product = product_seller.objects.get(prod_id=prod_id)
    data=customized_Designed.objects.all()
    if request.method == 'POST':
            product.image_src = request.FILES.get('final-image')
            product.tshirt_size = request.POST.get('tshirt_size')
            product.jsonfiles = request.FILES.get('jsonfiles')
            product.t_shirt_color = request.POST.get('t_shirt_color')
            product.tshirt_owndesign_s = request.FILES.get('cus-upload-image')

            # cust=Customize(image_src=image_src,tshirt_size=tshirt_size,jsonfiles=jsonfiles,t_shirt_color=t_shirt_color,tshirt_owndesign_s=tshirt_owndesign_s)
            product.save()

    context={
        'product':product,
        'data':data
    }

    return render(request,"customization/customization.html",context)


# clothing categories

def clothings(request):
    return render(request,"categories/clothing.html")

def tshirt(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts.html",context)

def shirts(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/shirts.html",context)

def kurtas(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses.html",context)

def sweatshirts(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/sweatshirts-and-hoodies.html",context)

def hoodies(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/hoodies.html",context)

def quote_tshirts(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",context)

def Signature_tshirts(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",context)


def BR_ambedkar_quotes(request):
    data=product_seller.objects.filter(sub_category="Babasaheb").order_by('-id')
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)

def Chrapati_shivaji_maharaj_quotes(request):
    data=product_seller.objects.filter(category="Shivaji")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)

def A_P_J_Abdul_kalam_tshirts(request):
    data=product_seller.objects.filter(sub_category="abdulkalam")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)

def Bhagat_Singh(request):
    data=product_seller.objects.filter(sub_category="bhagatsingh")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)



def Budha_quotes(request):
    data=product_seller.objects.filter(sub_category="buddha")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)

def Birsa_munda(request):
    data=product_seller.objects.filter(sub_category="birsamunda")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)

def Savitribai_Phule(request):
    data=product_seller.objects.filter(sub_category="savitribaiphule")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)


def Martin_Luther_King(request):
    data=product_seller.objects.filter(sub_category="martinluther")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)

def Sant_Kabir_Saheb(request):
    data=product_seller.objects.filter(sub_category="santkabir")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)

def Sri_Guru_Nanak_Dev_ji(request):
    data=product_seller.objects.filter(sub_category="gurunanak")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)

def Osho_quotes(request):
    data=product_seller.objects.filter(sub_category="osho")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)

def freedomandjustice(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-theme/freedom & justice/freedom_and_justice.html",context)

def equalityandinclusion(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-theme/Equality & Inclusion/equalityandinclusion.html",context)


def education_and_empowerment(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-theme/Education & Empowerment/educationandempowerment.html",context)

def Historical(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-time/Historical/by_time_historical.html",context)

def modern(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-time/Modern/by_time_modern.html",context)


def shop_by_national_region(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-region/National/by_region_national.html",context)

def shop_by_regional(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-region/Regional/by_regional.html",context)


def shop_by_profession_education(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-profession/Education & Social Work/Savitribaifule-es.html",context)

def shop_by_profession_arts(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-profession/Arts & Literature/Santkabir-al.html",context)

def shop_by_profession_science(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-profession/Science & Technology/profession_science_and_tecchnology.html",context)

# clothing Sub - categories


# t-shirts

def causespecifictees(request):
    return render(request,"categories/clothing-category/t-shirts-and-shirts/cause-specific-tees.html")

def graphictees(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",context)

def humorsatiretees(request):
    return render(request,"categories/clothing-category/t-shirts-and-shirts/humor-satire-tees.html")

def inspirationaltees(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",context)

def minimalisttees(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",context)


#kurtas

def comfortwear(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/comfort-wear.html",context)

def modernfusion(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/modern-fusion.html",context)

def occasionwear(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/occasion-wear.html",context)

def traditionaldesigns(request):
    data=product_seller.objects.filter(product_type="tshhirt")
    context={
    'data':data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/traditional-designs.html",context)

#hoodies


def croptopsfitted(request):
    return render(request,"categories/clothing-category/sweatshirts-and-hoodies/crop-tops-fitted.html")

def oversizedcozy(request):
    return render(request,"categories/clothing-category/sweatshirts-and-hoodies/oversized-cozy.html")

def slogansweatshirts(request):
    return render(request,"categories/clothing-category/sweatshirts-and-hoodies/slogan-sweatshirts.html")

def zipupspullovers(request):
    return render(request,"categories/clothing-category/sweatshirts-and-hoodies/zip-ups-pullovers.html")






# gits categories

def gifts(request):
    return render(request,"categories/gifts.html")

def themeBasedCollections(request):
    return render(request,"categories/gifts-category/themeBasedCollections.html")

def clothingTypeBlends(request):
    return render(request,"categories/gifts-category/clothingTypeBlends.html")

def productFocusedCombinations(request):
    return render(request,"categories/gifts-category/productFocusedCombinations.html")

def mixOfActivismEducation(request):
    return render(request,"categories/gifts-category/mixOfActivism&Education.html")

# gits sub-categories clothingTypeBlends

def causespecificscarfhatcombo(request):
    return render(request,"categories/gifts-category/clothingTypeBlends/cause-specific-scarf-hat-combo.html")

def empowermentkurtadress(request):
    return render(request,"categories/gifts-category/clothingTypeBlends/empowerment-kurta-dress.html")

def statementhoodietshirtset(request):
    return render(request,"categories/gifts-category/clothingTypeBlends/statement-hoodie-t-shirt-set.html")


# gits sub-categories mixOfActivism&Education

def educationalresources(request):
    return render(request,"categories/gifts-category/mixOfActivism&Education/educational-resources.html")

def postersprints(request):
    return render(request,"categories/gifts-category/mixOfActivism&Education/posters-prints.html")

def tshirtsapparel(request):
    return render(request,"categories/gifts-category/mixOfActivism&Education/t-shirts-apparel.html")


# gits sub-categories productFocusedCombinations

def activistessentialskit(request):
    return render(request,"categories/gifts-category/productFocusedCombinations/activist-essentials-kit.html")

def ecofriendly(request):
    return render(request,"categories/gifts-category/productFocusedCombinations/eco-friendly.html")

def jewelrygiftbox(request):
    return render(request,"categories/gifts-category/productFocusedCombinations/jewelry-gift-box.html")

# gits sub-categories themeBasedCollections

def educationwarriorpack(request):
    return render(request,"categories/gifts-category/themeBasedCollections/education-warrior-pack.html")

def equalitychampionscollection(request):
    return render(request,"categories/gifts-category/themeBasedCollections/equality-champions-collection.html")

def peacepilgrimbundle(request):
    return render(request,"categories/gifts-category/themeBasedCollections/peace-pilgrim-bundle.html")





# books

def books(request):
    data=product_seller.objects.filter(category="BK")
    context={
    'data':data,
    }
    return render(request,"categories/books.html",context)

#books sub-categories biographies-and-autobiographies

def biographiesautobiographies(request):
    return render(request,"categories/books-categories/biographies-and-autobiographies/biographies-autobiographies.html")

#books sub-categories childrens-books

def childrensbooks(request):
    return render(request,"categories/books-categories/childrens-books/childrens-books.html")

#books sub-categories fiction-and-poetry

def fictionandpoetry(request):
    return render(request,"categories/books-categories/fiction-and-poetry/fiction-and-poetry.html")

#books sub-categories social-justice

def socialjusticetexts(request):
    return render(request,"categories/books-categories/social-justice/social-justice-texts.html")

def socialjustice(request):
    return render(request,"social-justice/social-justice-texts.html")

# Paintings

def paintings(request):
    return render(request,"categories/paintings.html")




# painting categories

def limitededitionprints(request):
    return render(request,"categories/paintings-categories/limited-edition-prints/limited-edition-prints.html")

def localregionalartists(request):
    return render(request,"categories/paintings-categories/local-regional-artists/local-regional-artists.html")

def portraits(request):
    return render(request,"categories/paintings-categories/portraits/portraits.html")

def thematiccollections(request):
    return render(request,"categories/paintings-categories/thematic-collections/thematic-collections.html")

def biographiesandautobiographies(request):
    return render(request,"biographies-and-autobiographies/biographies-autobiographies.html")


def orders(request): 
    user=request.user   
    order = OrderPlaced.objects.filter(user=user)
    return render(request, "customer/orders.html", {'order': order})


def order_tracking(request,order_id):
    user = request.user
    order = OrderPlaced.objects.filter(user=user,order_id=order_id).first()
    print('gggggggggggggggggggggggggg',order)
  
    order_details = get_object_or_404(OrderPlaced, order_id=order_id)
    tracking_details = TrackingDetail.objects.filter(order=order_details).order_by('-date_time')


    return render(request, 'customer/order_tracking.html',{'order':order,'tracking_details':tracking_details})



def customer_order_report(request):
    user = request.user
    seller = user  # Assuming the seller is also a user in your system

    # Retrieve orders placed for products belonging to the seller
    orders = OrderPlaced.objects.filter(product__user=seller)

    context = {
        'orders': orders
    }
    return render(request, "seller/customer_order_report.html", context)



from django.http import HttpResponse

def cancel_order(request, order_id):
    try:
        order = OrderPlaced.objects.get(order_id=order_id)
    except OrderPlaced.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason')
        order.canceled = True
        order.cancel_reason = cancel_reason
        order.save()

        # Create a record of the canceled order
        CanceledOrder.objects.create(
            order_id=order.order_id,
            customer=order.customer,
            product=order.product,
            quantity=order.quantity,
            canceled_reason=cancel_reason
        )

        # Remove the order from the main list of orders
        order.delete()

        return redirect('/orders/')
    
    return render(request, "customer/cancel_orders.html", {'order': order})

def canceled_orders(request):
    canceled_orders = CanceledOrder.objects.filter(canceled=True).order_by('-canceled_at')
    return render(request, 'customer/canceled_orders.html', {'canceled_orders': canceled_orders})


def customize_plane_tshirt(request):
    

    all_data = product_seller.objects.filter(category="Customize")
       
    context ={
        'all_data': all_data,
        
    }
    return render(request,'customization/customize_plane_tshirt.html',context)


def filter_products(request, data=None):
    products = product_seller.objects.filter(brand='VR')  # Assuming default category is 'TS'

    if data == 'Clothes':
        products = products.filter(brand='VR')
    elif data == 'Accessories':
        products = products.filter(category='AC')
    elif data == 'Books':
        products = products.filter(category='BK')
    elif data == 'Painting':
        products = products.filter(category='PT')

    if data == '100_500':
        products = products.filter(discount_price__range=(100, 500))
    elif data == '600_1000':
        products = products.filter(discount_price__range=(600, 1000))
    elif data == 'above_1000':
        products = products.filter(discount_price__gte=1000)

    if data == 'price_low_to_high':
        products = products.order_by('discount_price')
    elif data == 'price_high_to_low':
        products = products.order_by('-discount_price')

    if data == 'red':
        products = products.filter(colour='red')
    elif data == 'green':
        products = products.filter(colour='green')

    return render(request, 'categories/clothing-category/t-shirts-and-shirts.html', {'data': products})
