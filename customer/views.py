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
from django.db import IntegrityError
from django.urls import reverse
from collections import defaultdict


@login_required(login_url='/customer_login/')
def add_cart(request,prod_id):
    user = request.user
    product = product_seller.objects.get(prod_id=prod_id)
    quantity = request.POST.get('quantity', 1)  # Default quantity is 1
    print('ffffffffffff',product.size)
    
    existing_cart_item = None
    if user.is_authenticated:
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
                    cart(user=user, product=product, quantity=quantity,size=product.size).save()
                    wish_data = Wishlist.objects.get(user=user, product=product)
                    wish_data.delete()
                else:
                    if not anonymous_user_id:
                        request.session.save()
                        anonymous_user_id = request.session.session_key
                    cart(anonymous_user_id=anonymous_user_id, product=product, quantity=quantity,size=product.size).save()
            except IntegrityError:
                messages.error(request, "An error occurred while adding the product to your cart.")
            
        return redirect('/view_wishlist/')
    else:
        return redirect('/customer_login/')


@login_required(login_url='/customer_login/')
def view_cart(request):
    user = request.user.username
    cart_items = cart.objects.filter(user__username=user).order_by('-id')
    data = Wishlist.objects.filter(user__username = user).order_by('-id')
        
    count = data.count()
    cart_count =cart_items.count()

    total_amount = 0.0
    for item in cart_items:
        item.product_price = item.quantity * item.product.selling_price
        # print('assssssssssssssssss',item.product_price)
        item.save()
        total_amount += item.quantity * item.product.selling_price
        total_amount = round(total_amount, 2)

    return render(request,'customer/cart.html',{'cart_items':cart_items,'total_amount':total_amount,'count':count,'cart_count':cart_count})
    
    
@login_required(login_url='/customer_login/')
def remove_cart(request,id):
    if request.method == 'GET':
        user = request.user
        c = cart.objects.get(id=id,user=user)
        c.delete()

    return redirect("/view_cart/") 


def move_to_wishlist(request, prod_id):
    user = request.user
    try:
        product = product_seller.objects.get(prod_id=prod_id)
    except product_seller.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect("/view_products/")  # Redirect to a suitable page

    existing_wishlist_item = Wishlist.objects.filter(user=user, product=product).first()

    if existing_wishlist_item:
        # If the product is already in the wishlist, display a message and redirect
        messages.warning(request, 'This product is already in your wishlist.')
        return redirect("/view_wishlist/")
    else:
        # If the product is not in the wishlist, add it
        wishlist = Wishlist(user=user, product=product)
        wishlist.save()

        cart_data = cart.objects.get(user=user,product=product)
        cart_data.delete()
        
        # Send email notification
        # subject = 'Product added to your wishlist.'
        # message = "\n Product added to your wishlist.\nBest regards,\nVR Team. "
        # from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
        # recipient_list = [user.email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return redirect("/view_cart/")


@login_required(login_url='/customer_login/')
def add_wishlist(request, prod_id):
    if request.method == 'POST':        
        user = request.user
        try:
            product = product_seller.objects.get(prod_id=prod_id)
        except product_seller.DoesNotExist:
            messages.error(request, 'Product not found.')
            return redirect("/view_products/")  # Redirect to a suitable page

        existing_wishlist_item = Wishlist.objects.filter(user=user, product=product).first()

        if existing_wishlist_item:
            # If the product is already in the wishlist, display a message and redirect
            messages.warning(request, 'This product is already in your wishlist.')
            return redirect("/")
        else:
            # If the product is not in the wishlist, add it
            wishlist = Wishlist(user=user, product=product)
            wishlist.save()
            
            # Send email notification
            subject = 'Product added to your wishlist.'
            message = "\n Product added to your wishlist.\nBest regards,\nVR Team. "
            from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            return redirect("/")

    return redirect("/") 


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
    product = product_seller.objects.get(prod_id=prod_id)
    reviews_count = Customer_Review.objects.filter(product=product).count()
    data_colour = product_seller.objects.filter(product_id=product.product_id) 
    print('ffffffffffff',data_colour)

    product_sellers = product_seller.objects.filter(product_id=product.product_id)

    # Create a set to store unique colors and a dictionary to store unique (prod_id, colour) pairs
    unique_colors = set()
    unique_prod_ids_and_colours = {}

    # Iterate through product_sellers to collect unique colours and (prod_id, colour) pairs
    for seller in product_sellers:
        if seller.colour not in unique_colors:
            unique_colors.add(seller.colour)
            unique_prod_ids_and_colours[seller.prod_id] = seller.colour


    # Retrieve sizes from product_seller objects
    sizes_list = [item.size for item in product_seller.objects.filter(product_id=product.product_id)]

    # Convert the list of sizes into a comma-separated string
    sizes1 = ', '.join(sizes_list)
    unique_sizes_set = set(sizes_list)
    
    # Convert the set of unique sizes into a comma-separated string
    sizes = ', '.join(unique_sizes_set)

    product_type = product.sub_category

    data_value=product_seller.objects.filter(sub_category=product_type)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    related_products = list(unique_product_ids.values())
    print('sssssssssssssssss',related_products)
    print('vvvvvvvvvvvvv',data_value)

    # related_products = product_seller.objects.filter(sub_category=product_type).order_by('-id')[:4]

    # Get products with the same type as the specified product
    similar_products = product_seller.objects.filter(product_type=product.product_type,title=product.title)
    product_colors = {}
    product_images = {}
    product_size = {}
    # print('aparnadddddddddddd',similar_products)
    # Extract color variations for each similar product

    # Colors aur images ko collect karna
    for similar_product in similar_products:
        colors = product_seller.objects.filter(product_type=similar_product.product_type, title=similar_product.title,product_id=similar_product.product_id).values_list('colour', flat=True)
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
        
        # review_condition=OrderPlaced.objects.filter(customer=request.user,product_id=prod_id)
        # print('reviewwwwwwwwww',review_condition,request.user)
    
        # Get the submitted review data
        name = request.POST.get('name')
        email = request.user.email
        review_star = request.POST.get('review_star')
        review_text = request.POST.get('review')
        customer_image = request.FILES.get('customer_image')

        # Save the review
        new_review = Customer_Review(product=product, name=name, email=email, review_star=review_star, review=review_text,customer_image=customer_image)
        new_review.save()

        name=prod_id
        url = reverse('prod_details', args=[prod_id])
        return redirect(url)

    # Calculate average rating and fetch reviews
    product_ratings = Customer_Review.objects.filter(product=product).aggregate(Avg('review_star'))['review_star__avg']
    average_rating = round(product_ratings) if product_ratings is not None else 0
    reviews = Customer_Review.objects.filter(product=product)
    total_reviews = reviews.count()
    star_ratings = {}

    star_counts = reviews.values('review_star').annotate(count=Count('review_star'))

    review_condition=''

    if request.user.is_authenticated:
        review_condition=OrderPlaced.objects.filter(user=request.user,product=product)
        print('reviewwwwwwwwww',review_condition,request.user)
        
    
    for star_count in star_counts:
        star_value = star_count['review_star']
        count = star_count['count']
        percentage = round((count / total_reviews) * 100)
        star_ratings[star_value] = percentage    

    # Check if the current user has already submitted a review for the current product
    # has_review = False
    if request.user.is_authenticated:
        user_review = Customer_Review.objects.filter(product=product,email=request.user.email).exists()

        user = request.user.username
        data = Wishlist.objects.filter(user__username = user).order_by('-id')

        count = data.count()
        # if user_review:
        #     has_review = True 

        context = {
            'available_colors': available_colors,
            #'tshirt_image_url': tshirt_image_url,
            'data':related_products,
            'average_rating': average_rating,
            'reviews': reviews,
            'star_ratings': star_ratings,
            'product': product,
            'prod_id': prod_id,
            'review_condition':review_condition,
            'reviews_count':reviews_count,
            'has_review':user_review,
            'data_colour':data_colour,
            'count':count,
            'sizes':sizes,
            'unique_colors': sorted(unique_colors),  # Sort colors alphabetically if desired
            'prod_ids_and_colours': unique_prod_ids_and_colours,
           
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
            'review_condition':review_condition,
            'reviews_count':reviews_count,
            'data_colour':data_colour,
            'sizes':sizes,
            'unique_colors': sorted(unique_colors),  # Sort colors alphabetically if desired
            'prod_ids_and_colours': unique_prod_ids_and_colours,
            
           
        }
        return render(request, 'product/prod_details.html', context)
         



from customer.models import *
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required(login_url='/customer_login/')
def checkout_view(request):
    discount_percent=0.0
    user = request.user
    add = customer_user.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    cart_items_count = cart_items.count()
    ship= 50
    for p in cart_items:
        p.product_price= p.quantity * p.product.selling_price

    mrp_amount = sum(p.quantity * p.product.selling_price for p in cart_items)
    total_amount_pre = mrp_amount
    tax = (mrp_amount * 18) / 100  # 18% tax
    coupon_code = None
    
    discount_on_mrp = 0.0
    grand_total = total_amount_pre + tax

    print('bbbbbbbbb',grand_total,tax,mrp_amount)
    
    discount_sources = [0.0]
        
    if request.user.is_authenticated:    
            first_order_condition=OrderPlaced.objects.filter(user=request.user)
            # print('orderrrrrrr',first_order_condition,request.user)
    
            if not first_order_condition:
                #discount_percent = 0.2  
                discount_sources.append(0.2)
                
            # Check for dynamically added event discount
            event_discount = Event.objects.filter(event_date=datetime.now().date()).values_list('event_discount', flat=True)
            if event_discount:
                event_discount = max(event_discount)  # Assuming only one event discount for the day
                #discount_percent =  event_discount  
                discount_sources.append(event_discount)  
                # print('gudhiiiiiiiiii',event_discount,discount_percent)
            
            if total_amount_pre >= 3000:
                 #discount_percent = 0.3
                 discount_sources.append(0.3)
        
            elif total_amount_pre >= 2000:
               # discount_percent = 0.25
               discount_sources.append(0.25)
         
            elif total_amount_pre >= 1500:
                 #discount_percent = 0.2
                 discount_sources.append(0.15)
       
            else:
                #discount_percent = 0.0
                discount_sources.append(0.0)
                
             # Get the maximum discount amount
            discount_percent = max(discount_sources)    
                
            # print('addition discountttttttt',discount_on_mrp)
            #if is_gudhi_padwa:
                  
    #discount_percent=max(discount_percent)
    discount_on_mrp = mrp_amount * discount_percent
    grand_total = grand_total - discount_on_mrp
    grand_totasl = grand_total - discount_on_mrp
    print('discount percentttttttttttt',discount_percent,discount_on_mrp,grand_total,grand_totasl,mrp_amount,discount_percent)    
        
    # print('ggggggggggggggggggg',grand_total)
    # print('ddddddddddddddddd',discount_on_mrp)
    
    pay = request.POST.get('flexRadioDefault')
    currency = 'INR'
    # amount = grand_total*100 # Rs. 200
    # print('amamamamam',amount)


    # we need to pass these details to frontend.
    context = {'mrp_amount': mrp_amount,
               'cart_items_count': cart_items_count,
               'add': add, 
               'cart_items': cart_items, 
               'discount_on_mrp': discount_on_mrp,
               'tax': tax, 
               'ship': ship, 
               'grand_total': grand_total,
               'coupon_code':coupon_code,
               'first_order_condition':first_order_condition,
               'event_discount':event_discount,
               }

    return render(request, 'customer/checkout.html', context=context)



from decimal import Decimal
def payment_method(request):
    total_amount=request.GET.get('total_amount')
    custid = request.GET.get('custid')
    # print("222222222222222222222222222222222222222",custid)
    user = request.user
    # print("111111111111111111111111111111111111111111111111111",user)
    cust = customer_user.objects.get(id=custid)
    cart_items = cart.objects.filter(user=cust.user)
    
    for p in cart_items:
        p.product_price= p.quantity * p.product.selling_price
    
    # cart_items = cart.objects.filter(user=user)

    for cart_item in cart_items:
        product = cart_item.product

        if int(product.quantity) <= 0:
            return HttpResponseBadRequest("One or more products in your cart are not available.")

        # Update the price field based on the product's discount price
        price = Decimal(product.discount_price)
        
    ship = Decimal('50')    
    cod=request.GET.get('COD')
    razorpay=request.GET.get('razorpay')
    if cod:  
        mrpamount = sum(Decimal(p.quantity) * Decimal(p.product.selling_price) for p in cart_items)
        tax = (mrpamount * Decimal('0.18'))
        ship = Decimal('50')
        totalamount = mrpamount + tax + ship
    else:
        mrpamount = sum(Decimal(p.quantity) * Decimal(p.product.selling_price) for p in cart_items)
        tax = (mrpamount * Decimal('0.18'))
        totalamount = mrpamount + tax
    
    
    
    discount_sources = [Decimal('0.0')]
        
    if request.user.is_authenticated:    
            first_order_condition=OrderPlaced.objects.filter(user=request.user)
            # print('orderrrrrrr',first_order_condition,request.user)
    
            if not first_order_condition:
                #discount_percent = 0.2  
                discount_sources.append(0.2)
                
            # Check for dynamically added event discount
            event_discount = Event.objects.filter(event_date=datetime.now().date()).values_list('event_discount', flat=True)
            if event_discount:
                event_discount = max(event_discount)  # Assuming only one event discount for the day
                #discount_percent =  event_discount  
                discount_sources.append(event_discount)  
                # print('gudhiiiiiiiiii',event_discount,discount_percent)
            
            if totalamount >= 3000:
                 #discount_percent = 0.3
                 discount_sources.append(0.3)
        
            elif totalamount >= 2000:
               # discount_percent = 0.25
               discount_sources.append(0.25)
         
            elif totalamount >= 1500:
                 #discount_percent = 0.2
                 discount_sources.append(0.15)
       
            else:
                #discount_percent = 0.0
                discount_sources.append(0.0)
                
             # Get the maximum discount amount
            discount_percent = max(discount_sources) 
            
    discount_on_mrp =Decimal('0.0') 
    grand_total = Decimal('0.0')    
    
    # Round discount_percent to 2 decimal places
    # discount_percent = discount_percent.quantize(Decimal('0.00'))
    
    # Convert discount_percent to Decimal
    discount_percent = Decimal(str(discount_percent))
        
    # discount_percent = Decimal(discount_percent)
    discount_on_mrp = mrpamount * discount_percent
    discount_on_mrp = discount_on_mrp.quantize(Decimal('0.00'))
    grand_total = grand_total - discount_on_mrp
    
    print("33333333333333333333333333333333333333333",discount_percent,discount_on_mrp)
    currency = 'INR'
    amount =  float(total_amount) * 100
    print('amamamamam',amount)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))
    
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    
    callback_url = f'http://127.0.0.1:8000/paymenthandler/?custid={custid}'
    # callback_url = f'http://vibetara.com/paymenthandler/?custid={custid}'

    context = {
        'amount':amount,
        'cust': cust,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price,
        'total_amount': total_amount,
        'totalamount': totalamount,
        'custid':custid,
        'grand_total':grand_total,
        'tax': tax, 
        'ship': ship,
        'discount_on_mrp':discount_on_mrp,
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
            cart_items_count = cart_items.count()
            ship= 50
            for p in cart_items:
                p.product_price= p.quantity * p.product.selling_price

            mrp_amount = sum(p.quantity * p.product.selling_price for p in cart_items)
            total_amount_pre = mrp_amount
            tax = (mrp_amount * 18) / 100  # 18% tax
            coupon_code = None
            
            discount_on_mrp = 0.0
            grand_total1 = total_amount_pre + tax
            discount_sources = [0.0]
        
            if request.user.is_authenticated:    
                    first_order_condition=OrderPlaced.objects.filter(user=request.user)
                    # print('orderrrrrrr',first_order_condition,request.user)
            
                    if not first_order_condition:
                        #discount_percent = 0.2  
                        discount_sources.append(0.2)
                        
                    # Check for dynamically added event discount
                    event_discount = Event.objects.filter(event_date=datetime.now().date()).values_list('event_discount', flat=True)
                    if event_discount:
                        event_discount = max(event_discount)  # Assuming only one event discount for the day
                        #discount_percent =  event_discount  
                        discount_sources.append(event_discount)  
                        # print('gudhiiiiiiiiii',event_discount,discount_percent)
                    
                    if total_amount_pre >= 3000:
                        #discount_percent = 0.3
                        discount_sources.append(0.3)
                
                    elif total_amount_pre >= 2000:
                    # discount_percent = 0.25
                         discount_sources.append(0.25)
                
                    elif total_amount_pre >= 1500:
                        #discount_percent = 0.2
                        discount_sources.append(0.15)
            
                    else:
                        #discount_percent = 0.0
                        discount_sources.append(0.0)
                        
                    # Get the maximum discount amount
                    discount_percent = max(discount_sources)    
                        
                    # print('addition discountttttttt',discount_on_mrp)
                    #if is_gudhi_padwa:
                        
            #discount_percent=max(discount_percent)
            discount_on_mrp = mrp_amount * discount_percent
            grand_total1 = grand_total1 - discount_on_mrp
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
                user = request.user

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

                subject = 'Purchase Confirmation from Vishwaratna.'
                message = "\n Thank you for your purchase on Vishwaratna! We are delighted to confirm that your order has been successfully processed.\nWe appreciate your trust in us for your shopping needs. If you have any questions or need further assistance, please don't hesitate to contact us.\nThank you for choosing Vishwaratna for your shopping experience!\n\nBest regards,\nVR Team. "
                from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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
                item.total_cost = grand_total1
                item.save()

    context = {
        'grand_total1': grand_total1,
        'tax': tax,
        'totalamount': totalamount,
        'data': data,
        'cust': cust,
        'order_id': order_id,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price,
        'discount_on_mrp':discount_on_mrp,
        'pay':pay,
    }
    login_url = "https://selloship.com/api/lock_actvs/Vendor_login_from_vendor_all_order"
    login_payload = {'email': 'sanjog.meshram@gmail.com', 'password': 'Kanu@0507'}
    login_headers = {'Authorization': '9f3017fd5aa17086b98e5305d64c232168052b46c77a3cc16a5067b'}
    
    try:
        login_response = requests.post(login_url, headers=login_headers, data=login_payload)
        login_data = login_response.json()
        print("login_data", login_data)
        
        if login_data.get('success') == '1':
            vendor_id = login_data.get('vendor_id')
            access_token = login_data.get('access_token')
            device_from = login_data.get('device_from')
            product_name = f"{order.product}, Size:{order.size}"
            print("99999999999",product_name)
            # Check if the order creation API response is successful
            order_url = "https://selloship.com/web_api/Create_order"
            order_payload = {
                'vendor_id': vendor_id,
                'device_from': device_from,
                'product_name': product_name,
                'price': str(grand_total1),
                'old_price': str(mrpamount),
                'first_name': cust.first_name,
                'last_name': cust.last_name,
                'mobile_no': cust.mobile_number,
                'email': cust.user.email,
                'address': cust.locality,
                'state': cust.state,
                'city': cust.city,
                'zip_code': cust.pincode,
                
                'payment_method': 4,
                'qty': order.quantity,
                'custom_order_id': order.order_id,
            }
            print("0000000000000000000000000",order_payload)
            order_headers = {'Authorization': access_token, 'Cookie': 'AWSALB=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; AWSALBCORS=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; ci_session=pqh3eqv8k7o4ruvmc4b1bvqbhv66arjv'}
            
            try:
                order_response = requests.post(order_url, headers=order_headers, data=order_payload)
                print("order_response response:", order_response.text)

                data = OrderPlaced.objects.filter(user=user, order_id=order_id)
                if order_response.status_code == 200:
                    order_data = order_response.json()
                    if order_data.get('success') == '1':
                        selloship_order_id = order_data.get('selloship_order_id')
                        selloship_url = order_data.get('selloship_url')
                        print("11111",selloship_url,selloship_order_id)
                        
                        order.selloship_id = selloship_order_id  # Replace your_order_id with the actual order ID

                        # Update the selloship_order_id field
                        
                        order.save()
                        print("mmmmmmmmmmmmm",order)
                        
                        # Use the order data as needed, for example, redirect to the order view URL
                        return render(request, "customer/order_success.html",context)
                    else:
                        return JsonResponse({'error': 'Order creation failed'}, status=500)
                else:
                    return JsonResponse({'error': 'Failed to create order'}, status=order_response.status_code)
            except Exception as e:
                print("Error creating order:", e)
                return JsonResponse({'error': 'An error occurred while creating order'}, status=500)
        else:
            return JsonResponse({'error': 'Login failed'}, status=401)
    except Exception as e:
        print("Error logging in:", e)
        return JsonResponse({'error': 'An error occurred while logging in'}, status=500)






def add_to_cart(request):
    if request.method == 'POST':
        prod_id= request.POST.get('prod_id')
        if request.POST.get('action') == 'add_to_cart':
            user = request.user
            prod_id = request.POST.get('prod_id')
            product = product_seller.objects.get(prod_id=prod_id)
            quantity = request.POST.get('quantity', 1)  # Default quantity is 1
            size = request.POST.get('size')
            
            existing_cart_item = None
            if user.is_authenticated:
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
                            subject = 'Product added to your Cart.'
                            message = "\n Product added to your cart.\nBest regards,\nVR Team. "
                            from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
                            recipient_list = [user]
                            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                        else:
                            if not anonymous_user_id:
                                request.session.save()
                                anonymous_user_id = request.session.session_key
                            cart(anonymous_user_id=anonymous_user_id, product=product, quantity=quantity, size=size).save()
                    except IntegrityError:
                        messages.error(request, "An error occurred while adding the product to your cart.")
                data = prod_id
                url = reverse('prod_details', args=[data])
                print('Generated URL:', url)           
                return redirect(url)
                # return redirect('/view_cart/')
            else:
                return redirect('/customer_login/')
        
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
        elif request.POST.get('action') == 'add_to_wishlist':      
            user = request.user
            prod_id = request.POST.get('prod_id')
            product = product_seller.objects.get(prod_id=prod_id)
            existing_wishlist_item = Wishlist.objects.filter(user=user, product=product).first()

          
            if existing_wishlist_item:
                # If the product is already in the wishlist, display a message and redirect
                messages.warning(request, 'This product is already in your wishlist.')
                data = prod_id
                url = reverse('prod_details', args=[data])
                print('Generated URL:', url)           
                return redirect(url)
                # return redirect("/view_wishlist/")
            else:
                # If the product is not in the wishlist, add it
                wishlist = Wishlist(user=user, product=product)
                wishlist.save()
                subject = 'Product added to your wishlist.'
                message = "\n Product added to your wishlist.\nBest regards,\nVR Team. "
                from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
                recipient_list = [user]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Product added to your wishlist.')
                data = prod_id
                url = reverse('prod_details', args=[data])
                print('Generated URL:', url)           
                return redirect(url)
                # return redirect("/view_wishlist/")
     
    data = prod_id
    url = reverse('customer_before_login', args=[data])
    print('Generated URL:', url)           
    return redirect(url)

    

def save_address1(request):
    if request.method == 'POST':
        # Extract data from the POST request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        mobile_number = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        print('ooooooooooooooooooooooooooo',first_name,last_name,mobile_number,email,locality,city,state,pincode)
        # Create a new Customer object and save it to the database
        customer = customer_user(
            user=request.user,  # Assuming you have a logged-in user
            first_name=first_name,
            email=email,
            last_name=last_name,
            mobile_number=mobile_number,
            locality=locality,
            city=city,
            state=state,
            pincode=pincode)
        
        customer.save()
    return redirect('/checkout/')


def calculate_delivery_date(order_date):
    # Assuming a fixed delivery time of 5 days for simplicity
    delivery_time = timedelta(days=5)
    estimated_delivery_date = order_date + delivery_time
    return estimated_delivery_date



@login_required(login_url='/customer_login/')
def create_order(request):
    total_amount=request.GET.get('total_amount')
    custid = request.GET.get('custid')
    user = request.user
    pay = request.GET.get('COD')
    cust = customer_user.objects.get(id=custid)
    
    cart_items = cart.objects.filter(user=cust.user)
    
    characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
    order_id = ''.join(random.choices(characters, k=6))

    characters_upper = string.ascii_uppercase 
    characters_digits = string.digits  
    first_three_chars = ''.join(random.choices(characters_upper, k=3))
    remaining_digits = ''.join(random.choices(characters_digits, k=7))
    invoice_id = f'{first_three_chars}{remaining_digits}'

    # order = OrderPlaced.objects.get(order_id=order_id)
    # estimated_delivery_date = calculate_delivery_date(order.Order_date)
   
    
    for cart_item in cart_items:
        product = cart_item.product

        if int(product.quantity) <= 0:
            return HttpResponseBadRequest("One or more products in your cart are not available.")

        # Update the price field based on the product's discount price
        price = Decimal(product.discount_price)

        # Calculate total price for the product based on selling price and quantity
        product_price = Decimal(product.selling_price) * cart_item.quantity

        # Calculate tax for the product
        tax = product_price * Decimal('0.18')
        print('taaaaaaaaaaaaaaaaaaax',tax)

        # Calculate total cost for the product (including tax and shipping charges)
        total_cost = product_price + tax + Decimal('50')
        
        order = OrderPlaced.objects.create(
            user=user,
            customer=cust,
            product=product,
            quantity=cart_item.quantity,
            size=cart_item.size,
            price=price,  # Use discount price for online payment
            order_id=order_id,
            payment_method=pay,
            invoice_no=invoice_id,
            tax=tax,
            product_price=product_price,
            total_cost=total_cost,
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
    ship_charge1 = 50
    total_amount_float = float(total_amount)
    ship_charge = str(50)
    print('vvvvvvvv',type(total_amount),type(total_amount_float),type(ship_charge1))
    total_data = total_amount_float + ship_charge1
    
    for item in data:
        print('total_data',total_data)
        item.total_cost = total_data
        item.save()

    subject = 'Purchase Confirmation from Vishwaratna.'
    message = "\n Thank you for your purchase on Vishwaratna! We are delighted to confirm that your order has been successfully processed.\nWe appreciate your trust in us for your shopping needs. If you have any questions or need further assistance, please don't hesitate to contact us.\nThank you for choosing Vishwaratna for your shopping experience!\n\nBest regards,\nVR Team. "
    from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
    recipient_list = [cust.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    customer_name = f"{cust.first_name} {cust.last_name}"
    customer_address = f"{cust.locality}, {cust.city}, {cust.pincode}, {cust.state}"

    product_details = []
    for cart_item in cart_items:
        product_name = cart_item.product.title
        quantity = cart_item.quantity
        order_amount = total_amount
        product_details.append(f"{product_name}: {quantity}")
        
    payment_method = pay  # Payment method from the request
    invoice_number = invoice_id  # Invoice number generated in the view    

    # Sending email to admin
    admin_email = 'vishwaratnasite@gmail.com'
    admin_subject = 'New Order Placed From Customer'
    admin_message = f"New Order Placed:\n\nOrder Amount: {order_amount}\nCustomer Name: {customer_name}\nCustomer Address: {customer_address}\n\nProduct Details:\n"
    admin_message += "\n".join(product_details)
    admin_message += f"\n\nPayment Method: {payment_method}\nInvoice Number: {invoice_number}"

    
    send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [admin_email])

    print('bbbbbbbbbbbbbb',total_amount,totalamount,ship,total_data)
    email_context = {
        'order_items': data,
        'order_total': total_amount,
        'order_tax': tax,
        'order_shipping': ship,
        'order_grand_total': total_amount,
    }
    discount_on_mrp = 0
    context = {
        'grand_total1': total_data,
        'tax': tax,
        'totalamount': totalamount,
        'data': data,
        'cust': cust,
        'order_id': order_id,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price,
        'discount_on_mrp':discount_on_mrp,
        'pay':pay
    }
    
    return render(request, "customer/order_success.html", context)


from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField
from num2words import num2words  # Import the num2words library for converting numbers to words



def invoice(request, order_id):
    
    # custid = request.GET.get('custid')
    user = request.user
    
    # Assuming you have a tax rate, replace 0.1 with your actual tax rate
    order = OrderPlaced.objects.filter(user=user, order_id=order_id)
  
    # cust = customer_user.objects.get(id=custid)  
    # Calculate the net amount for each item (total_cost - tax - shipping charges)
    order = order.annotate(net_amount=ExpressionWrapper(
        F('total_cost') - F('tax') - 50, output_field=DecimalField()
    ))
      
    
    # Calculate the total cost of all items in the order
    total_cost = order.aggregate(total_cost=Sum('total_cost'))['total_cost']

    order_cost = OrderPlaced.objects.filter(user=user, order_id=order_id).last()
    print('vvvvvvvvv',order_cost.total_cost)
    
    # Convert total_cost to words
    total_cost_in_words = num2words(order_cost.total_cost, lang='en').title()  # Convert to title case for better readability
    
    
    
    return render(request, "customer/invoice.html", {'order': order, 'total_cost':total_cost,'total_cost_in_words':total_cost_in_words,'order_cost':order_cost})


@login_required(login_url='/customer_login/')
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


# @login_required(login_url='/customer_login/')
# def return_order(request, order_id):
#     order = OrderPlaced.objects.get(order_id=order_id)
#     if request.method == 'POST':
#         return_reason = request.POST.get('return_reason')
#         order.returned = True
#         order.return_reason = return_reason 
#         order.save()
        
#         order_items = OrderPlaced.objects.filter(order_id=order_id)
#         for item in order_items:
#             product = item.product
#             quantity_ordered = item.quantity
#             product.quantity = F('quantity') + quantity_ordered
#             product.save()
            
#         return redirect('/orders/')  
#     return render(request, 'customer/return_orders.html', {'order': order})

@login_required(login_url='/customer_login/')
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
            
            # Send email to customer about return request
        subject = f'Return Request Received - Vibetara Order #{order.order_id}'
        message = f"Hi {order.customer.first_name},\n\n"
        message += f"We've received your return request for order #{order.order_id}.\n\n"
        message += "Our team will review your request and get back to you shortly with further instructions on the return process.\n\n"
        message += "Thank you for choosing Vibetara. We appreciate your understanding and cooperation.\n\n"
        message += "Best regards,\nThe Vibetara Team"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.customer.email]

        send_mail(subject, message, from_email, recipient_list)

            
        return redirect('/orders/')  
    return render(request, 'customer/return_orders.html', {'order': order})   
    

def customization(request, prod_id):
    product = product_seller.objects.get(prod_id=prod_id)
    data = customized_Designed.objects.all()

    if request.method == 'POST':
        # Update product with new customization details
        product.image_src = request.FILES.get('final-image')
        product.tshirt_size = request.POST.get('tshirt_size')
        product.jsonfiles = request.FILES.get('jsonfiles')
        product.t_shirt_color = request.POST.get('t_shirt_color')
        product.tshirt_owndesign_s = request.FILES.get('cus-upload-image')

        # Save the product
        product.save()

        user = request.user
        print('hhj',user)
        # prod_id = request.POST.get('prod_id')
        product = product_seller.objects.get(prod_id=prod_id)
        print('xzzzzzzzzzzzzzzzzz',product.jsonfiles    )
        quantity = request.POST.get('quantity', 1)  # Default quantity is 1
        size = request.POST.get('tshirt_size')
        image_src = request.FILES.get('final-image')
        
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
                    cart(user=user, product=product, quantity=quantity, size=size,image_src=image_src).save()
                else:
                    if not anonymous_user_id:
                        request.session.save()
                        anonymous_user_id = request.session.session_key
                    cart(anonymous_user_id=anonymous_user_id, product=product, quantity=quantity, size=size,image_src=image_src).save()


            except IntegrityError:
                messages.error(request, "An error occurred while adding the product to your cart.")

        return redirect('/view_cart/')

    context = {
        'product': product,
        'data': data,
        'prod_id':prod_id,
    }
    
    return render(request, "customization/customization_old.html", context)


# clothing categories

def clothings(request):
    return render(request,"categories/clothing.html")

from collections import defaultdict
def tshirt(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="tshirt")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "tshirt":
            print("khshjhj",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)

    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)
    data=product_seller.objects.filter(product_type="T-shirt")
    context={
    'data':unique_data,
    'data1':data1,
    }

    return render(request,"categories/clothing-category/t-shirts-and-shirts.html",context)


def shirts(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="tshirt")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "tshirt":
            print("khshjhj",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)

    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/shirts.html",context)


def kurtas(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="tshirt")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "tshirt":
            print("khshjhj",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)

    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses.html",context)

def sweatshirts(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="tshirt")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "tshirt":
            print("khshjhj",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)

    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/sweatshirts-and-hoodies.html",context)

def hoodies(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="tshirt")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "tshirt":
            print("khshjhj",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)

    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/hoodies.html",context)

def quote_tshirts(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="quote_tshirts")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "quote_tshirts":
            print("jghjsgdjghg",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",context)


def Signature_tshirts(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="Signature_tshirts")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Signature_tshirts":
            print("jghjsgdjghg",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)

    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",context)


def BR_ambedkar_quotes(request):
    data_value=product_seller.objects.filter(sub_category="Babasaheb").order_by('-id')
    data1= Collections_Thought.objects.filter(subcategory="BR_ambedkar_quotes")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "BR_ambedkar_quotes":
            print("1111111",i.subcategory)
    unique_product_ids = defaultdict(lambda: None)      
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)

    context={
    'data':unique_data,
    'data1':data1,
    }

    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)


def Chrapati_shivaji_maharaj_quotes(request):
    data_value=product_seller.objects.filter(category="Shivaji")
    data1= Collections_Thought.objects.filter(subcategory="Chrapati_shivaji_maharaj_quotes")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Chrapati_shivaji_maharaj_quotes":
            print("2222222222",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)


def A_P_J_Abdul_kalam_tshirts(request):
    data_value=product_seller.objects.filter(sub_category="abdulkalam")
    data1= Collections_Thought.objects.filter(subcategory="A_P_J_Abdul_kalam_tshirts")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "A_P_J_Abdul_kalam_tshirts":
            print("333",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)


def Bhagat_Singh(request):
    data_value=product_seller.objects.filter(sub_category="bhagatsingh")
    data1= Collections_Thought.objects.filter(subcategory="Bhagat_Singh")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Bhagat_Singh":
            print("44444444",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)


def Budha_quotes(request):
    data_value=product_seller.objects.filter(sub_category="buddha")
    data1= Collections_Thought.objects.filter(subcategory="Budha_quotes")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Budha_quotes":
            print("555555",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)


def Birsa_munda(request):
    data_value=product_seller.objects.filter(sub_category="birsamunda")
    data1= Collections_Thought.objects.filter(subcategory="Birsa_munda")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Birsa_munda":
            print("66666666",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)


def Savitribai_Phule(request):
    data_value=product_seller.objects.filter(sub_category="savitribaiphule")
    data1= Collections_Thought.objects.filter(subcategory="Savitribai_Phule")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Savitribai_Phule":
            print("777777777777",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)


def Martin_Luther_King(request):
    data_value=product_seller.objects.filter(sub_category="martinluther")
    data1= Collections_Thought.objects.filter(subcategory="Martin_Luther_King")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Martin_Luther_King":
            print("88888888888888888888",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)


def Sant_Kabir_Saheb(request):
    data_value=product_seller.objects.filter(sub_category="santkabir")
    data1= Collections_Thought.objects.filter(subcategory="Sant_Kabir_Saheb")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Sant_Kabir_Saheb":
            print("9999999999",i.subcategory)

    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }

    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)


def Sri_Guru_Nanak_Dev_ji(request):
    data_value=product_seller.objects.filter(sub_category="gurunanak")
    data1= Collections_Thought.objects.filter(subcategory="Sri_Guru_Nanak_Dev_ji")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Sri_Guru_Nanak_Dev_ji":
            print("00000000000",i.subcategory)

    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)


def Osho_quotes(request):
    data_value=product_seller.objects.filter(sub_category="osho")
    data1= Collections_Thought.objects.filter(subcategory="Osho_quotes")
    for i in data1:
        print("data1",i.subcategory)
        if i.subcategory == "Osho_quotes":
            print("00000000000",i.subcategory)

    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)


def freedomandjustice(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-theme/freedom & justice/freedom_and_justice.html",context)


def equalityandinclusion(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-theme/Equality & Inclusion/equalityandinclusion.html",context)


def education_and_empowerment(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-theme/Education & Empowerment/educationandempowerment.html",context)


def Historical(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-time/Historical/by_time_historical.html",context)

def modern(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-time/Modern/by_time_modern.html",context)


def shop_by_national_region(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-region/National/by_region_national.html",context)


def shop_by_regional(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-region/Regional/by_regional.html",context)


def shop_by_profession_education(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-profession/Education & Social Work/Savitribaifule-es.html",context)

def shop_by_profession_arts(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-profession/Arts & Literature/Santkabir-al.html",context)

def shop_by_profession_science(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/featuredReformers-category/by-profession/Science & Technology/profession_science_and_tecchnology.html",context)

# clothing Sub - categories


# t-shirts

def causespecifictees(request):
    return render(request,"categories/clothing-category/t-shirts-and-shirts/cause-specific-tees.html")

def graphictees(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="graphictees")
    for i in data1:
        if i.subcategory == "graphictees":
            print("gjhghjgjhgjg",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }

    return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",context)


def humorsatiretees(request):
    return render(request,"categories/clothing-category/t-shirts-and-shirts/humor-satire-tees.html")

def inspirationaltees(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="inspirationaltees")
    for i in data1:
        if i.subcategory == "inspirationaltees":
            print("rerwwreweee",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }    
    return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",context)


def minimalisttees(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    data1= Collections_Thought.objects.filter(subcategory="minimalisttees")
    for i in data1:
        if i.subcategory == "minimalisttees":
            print("jhghgfhtdhdresweeser",i.subcategory)
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    'data1':data1,
    }
    return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",context)



#kurtas

def comfortwear(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/comfort-wear.html",context)

def modernfusion(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/modern-fusion.html",context)

def occasionwear(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
    }
    return render(request,"categories/clothing-category/kurtas-and-dresses/occasion-wear.html",context)

def traditionaldesigns(request):
    data_value=product_seller.objects.filter(product_type="T-shirt")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
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
    data_value=product_seller.objects.filter(category="BK")
    unique_product_ids = defaultdict(lambda: None) 
    for entry in data_value:
        if entry.product_id not in unique_product_ids:
            unique_product_ids[entry.product_id] = entry

    # Convert the dictionary values back to a list to maintain the queryset structure
    unique_data = list(unique_product_ids.values())
    print('sssssssssssssssss',unique_data)
    print('vvvvvvvvvvvvv',data_value)    
    context={
    'data':unique_data,
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
    for i in order:
        product = product_seller.objects.get(pk=i.product_id)  
        i.selling_price = product.selling_price
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

    print('bbbbbbbbbb',order.payment_method)
    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason')

        if order.payment_method =="Razorpay":
                # Initialize Razorpay client
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Fetch the payment ID associated with the order
            payment_id = order.razorpay_payment_id

            user=request.user
            
            try:
                # Initiate refund for the payment
                refund_response = razorpay_client.payment.refund(payment_id, { 'amount': int(float(order.total_cost) * 100) })
                # Check refund status
                if refund_response['status'] == 'processed':
                    # Refund successful, proceed with canceling the order
                    order.canceled = True
                    order.cancel_reason = cancel_reason
                    order.save()

                    # Create a record of the canceled order
                    CanceledOrder.objects.create(
                        order_id=order.order_id,
                        customer=order.customer,
                        product=order.product,
                        quantity=order.quantity,
                        canceled_reason=cancel_reason,
                        payment_method=order.payment_method,
                        invoice_no=order.invoice_no,
                        total_cost=order.total_cost,
                        razorpay_order_id=order.razorpay_order_id,
                        razorpay_payment_id=order.razorpay_payment_id 
                    )

                    # Remove the order from the main list of orders
                    
                    order.delete()
                    
                    subject = 'cancel orders payment Refund .'
                    message = "\n Cancel orders Payment Refunded to your account.\nBest regards,\nVR Team. "
                    from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


                    return redirect('/orders/')
                else:
                    # Refund failed, handle the error
                    return HttpResponse("Refund failed", status=500)  # You can customize this error response as needed
                
            except Exception as e:
                # Handle exceptions
                return HttpResponse("Refund failed: " + str(e), status=500)  # You can customize this error response as needed
        else:
            order.canceled = True
            order.cancel_reason = cancel_reason
            order.save()

            # Create a record of the canceled order
            CanceledOrder.objects.create(
                order_id=order.order_id,
                customer=order.customer,
                product=order.product,
                quantity=order.quantity,
                canceled_reason=cancel_reason,
                payment_method=order.payment_method,
                invoice_no=order.invoice_no,
                total_cost=order.total_cost 
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


def customer_blog_details(request,id):
    blog = BlogPost.objects.get(pk=id)
    return render(request, 'blogs/customer_blogs.html',{'blog':blog})




def tshirt_male(request):
    gender = request.GET.get('gender')
    print('gender',gender)
    data = product_seller.objects.filter(gender="male")
    context={
        'data':data,
    }
    if gender == 'tshirt':
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)
    elif gender == 'quote':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",context)
    elif gender == 'graphic':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",context)
    elif gender == 'signature':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",context)
    elif gender == 'minimalist':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",context)
    elif gender == 'inspiration':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",context)
    else:
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)
        

def tshirt_female(request):
    gender = request.GET.get('gender')
    print('gender',gender)
    data = product_seller.objects.filter(gender="female")
    context={
        'data':data,
    }
    if gender == 'tshirt':
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)
    elif gender == 'quote':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",context)
    elif gender == 'graphic':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",context)
    elif gender == 'signature':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",context)
    elif gender == 'minimalist':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",context)
    elif gender == 'inspiration':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",context)
    else:
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)

    



from django.shortcuts import render
from .models import product_seller

def filter_products(request, data=None):

    price = request.GET.get('price')
    # Retrieve products based on the 'data' parameter
    products = product_seller.objects.filter(product_type="T-shirt")

    if data == 'Clothes':
        products = products.filter(category='Clothes')

    # Apply filtering based on 'data' parameter
    if data == '100_500':
        products = products.filter(selling_price__range=(100, 500))
    elif data == '600_1000':
        products = products.filter(selling_price__range=(600, 1000))
    elif data == 'above_1000':
        products = products.filter(selling_price__gte=1000)

    # Filter products based on 'gender' query parameter
    gender = request.GET.get('gender')
    if gender:
        gender = gender.lower()
        products = products.filter(gender=gender)

    # Apply sorting based on the 'sorting' parameter
    if data == 'price_low_to_high':
        products = products.order_by('selling_price')
    elif data == 'price_high_to_low':
        products = products.order_by('-selling_price')


    if price == 'tshirt_price':
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html', {'data': products})
    elif price == 'quote_price':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",{'data': products})
    elif price == 'graphic_price':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",{'data': products})
    elif price == 'signatur_price':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",{'data': products})
    elif price == 'minimalist_price':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",{'data': products})
    elif price == 'inspiration_price':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",{'data': products})
    else:
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html', {'data': products})



from datetime import datetime, time
from datetime import datetime, timedelta
def filter_colour(request,data):

    print('Shirt Value:', data)
    pro_data=product_seller.objects.all()

    selected_colors = request.GET.getlist('colour')
    print('hhhhhhhhbbbbbbbbbbbbbbbbbbbbbb',selected_colors )
    if selected_colors:
        filtered_products = pro_data.filter(colour__in=selected_colors)
      
    products = filtered_products

    context = {
        'data': products,
    }

    if data == 'tshirt':
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)
    elif data == 'quote':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",context)
    elif data == 'graphic':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",context)
    elif data == 'signatur':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",context)
    elif data == 'minimalist':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",context)
    elif data == 'inspiration':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",context)
    else:
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)



def filter_size(request,size):
    pro_data=product_seller.objects.all()
    print('HGGGGGGGGGG',pro_data)
    selected_sizes = request.GET.getlist('size')
    print('bncbnvcnvbncbvncbnmbcmnbvmn',selected_sizes)
    if selected_sizes:
        filtered_products = []
        for size in selected_sizes:
            filtered_products.extend(pro_data.filter(size__iexact=size))
            print('hhhhhhhhhhhhhhhhhhhhh',filtered_products)
        products = filtered_products
        print('mmmmmmmmmmmmmmmmmmmmmm',products)

    context = {
        'data': products,
    }
    if size == 'tshirt':
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)
    elif size == 'quote':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quote-t-shirts.html",context)
    elif size == 'graphic':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/graphic-tees.html",context)
    elif size == 'signatur':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/signature-t-shirts.html",context)
    elif size == 'minimalist':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/minimalist-tees.html",context)
    elif size == 'inspiration':
        return render(request,"categories/clothing-category/t-shirts-and-shirts/inspirational-tees.html",context)
    else:
        return render(request, 'categories/clothing-category/t-shirts-and-shirts.html',context)



from datetime import datetime, time
from datetime import datetime, timedelta
def filter(request):
    products = product_seller.objects.filter(product_type="T-shirt")
    current_datetime = datetime.now()

    start_date = current_datetime - timedelta(days=10)

    products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime))

    for i in products:
        print('vvvvvvvvvvvvvvvv',i.product_date,type(i.product_date))
    

    sub_categories = product_seller.objects.values_list('sub_category', flat=True).distinct()
    print('lllllllllll',sub_categories)

    

    products = product_seller.objects.all()
    selected_discount_ranges = request.GET.getlist('discount_percentage')
    print('wwwwwwwwwwwwwwwwwwwwwww',selected_discount_ranges)
    filtered_products = []  # Initialize filtered_products here
    if selected_discount_ranges:
        print('selected_discount_ranges',selected_discount_ranges)
        for discount_range in selected_discount_ranges:
            print('kkkkkkkkkkkkkkkkkkkkkkkk')
            if "5%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=5, discount_percentage__lt=10))
                print("Filtered Products (5% or more):", filtered_products)
            elif "10%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=10, discount_percentage__lt=20))
            elif "20%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=20, discount_percentage__lt=30))
            elif "30%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=30, discount_percentage__lt=40))
            elif "40%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=40, discount_percentage__lt=50))
            elif "50%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=50, discount_percentage__lt=60))

            elif "60%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=60, discount_percentage__lt=70))

            elif "70%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=70, discount_percentage__lt=80))

            elif "80%" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=80, discount_percentage__lt=90))
            elif "90" in discount_range:
                filtered_products.extend(products.filter(discount_percentage__gte=90))
                print("Filtered Products (90% or more):", filtered_products)
                
        products = filtered_products
    return render(request, 'categories/clothing-category/t-shirts-and-shirts.html', {'data': products,'sub_categories': sub_categories})


# new 25april

from django.shortcuts import redirect, render, get_object_or_404
from .models import Customer_Review, product_seller  

@login_required(login_url='/customer_login/')
def update_reviews(request, prod_id,id):
    product = get_object_or_404(product_seller, prod_id=prod_id)
    reviews_data = Customer_Review.objects.filter(product=product)
    reviews = Customer_Review.objects.get(id=id)
    
    if request.method == 'POST':
        # Assuming the review ID is submitted along with the form data
        review_id = request.POST.get('review_id')
        
        print('Review ID:', review_id)
        user=request.user.first_name
       
        reviews.name = user
        # reviews.email=user_email
        reviews.review_star = request.POST.get('review_star')
        reviews.review = request.POST.get('review')

        reviews.save()

        return redirect('prod_details', prod_id=prod_id)

    context = {
        'reviews': reviews,
    }
    return render(request, 'customer/edit_reviews.html', context)



def collection_male(request):
    gender = request.GET.get('gender')
    # print('gendeeeeeeeeeeeeeer',gender)
    sub_category=request.GET.get('sub_category')
    # print('subcat',sub_category)
    if gender == 'male' and sub_category =='Chrapati_shivaji_maharaj_quotes':
        data = product_seller.objects.filter(gender="male",sub_category='Shivaji')
        context={
                'data':data,
            }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
    
    
    elif gender=='male'and sub_category=='BR_ambedkar_quotes':
        data = product_seller.objects.filter(gender="male",sub_category='Babasaheb')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
    elif gender=='male'and sub_category=='bhagatsingh':
        data = product_seller.objects.filter(gender="male",sub_category='bhagatsingh')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
    elif gender=='male'and sub_category=='abdulkalam':
        data = product_seller.objects.filter(gender="male",sub_category='abdulkalam')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
    elif gender=='male'and sub_category=='gurunanak':
        data = product_seller.objects.filter(gender="male",sub_category='gurunanak')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
    elif gender=='male'and sub_category=='osho':
        data = product_seller.objects.filter(gender="male",sub_category='osho')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
    elif gender=='male'and sub_category=='savitribaiphule':
        data = product_seller.objects.filter(gender="male",sub_category='savitribaiphule')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
    elif gender=='male'and sub_category=='birsamunda':
        data = product_seller.objects.filter(gender="male",sub_category='birsamunda')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
    elif gender=='male'and sub_category=='buddha':
        data = product_seller.objects.filter(gender="male",sub_category='buddha')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
    elif gender=='male'and sub_category=='santkabir':
        data = product_seller.objects.filter(gender="male",sub_category='santkabir')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
    elif gender=='male'and sub_category=='martinluther':
        data = product_seller.objects.filter(gender="male",sub_category='martinluther')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)

    else:
        data = product_seller.objects.filter(gender="male",sub_category='Shivaji')
        context={
                'data':data,
            }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)


def tshirt_female_shivaji_maharaj(request):
    gender = request.GET.get('gender')
    sub_category=request.GET.get('sub_category')
    
    print('gender',gender)
    print('sub_category',sub_category)
    if gender == 'female' and sub_category =='Chrapati_shivaji_maharaj_quotes':
        data = product_seller.objects.filter(gender="female",sub_category='Shivaji')
        context={
                'data':data,
            }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
    elif gender=='female'and sub_category=='BR_ambedkar_quotes':
        data = product_seller.objects.filter(gender="female",sub_category='Babasaheb')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
    elif gender=='female'and sub_category=='A_P_J_Abdul_kalam_tshirts':
        data = product_seller.objects.filter(gender="female",sub_category='abdulkalam')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
    elif gender=='female'and sub_category=='bhagatsingh':
        data = product_seller.objects.filter(gender="female",sub_category='bhagatsingh')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
    elif gender=='female'and sub_category=='gurunanak':
        data = product_seller.objects.filter(gender="female",sub_category='gurunanak')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
    elif gender=='female'and sub_category=='osho':
        data = product_seller.objects.filter(gender="female",sub_category='osho')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
    elif gender=='female'and sub_category=='savitribaiphule':
        data = product_seller.objects.filter(gender="female",sub_category='savitribaiphule')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
    elif gender=='female'and sub_category=='birsamunda':
        data = product_seller.objects.filter(gender="female",sub_category='birsamunda')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
    elif gender=='female'and sub_category=='buddha':
        data = product_seller.objects.filter(gender="female",sub_category='buddha')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
    elif gender=='female'and sub_category=='santkabir':
        data = product_seller.objects.filter(gender="female",sub_category='santkabir')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
    elif gender=='female'and sub_category=='martinluther':
        data = product_seller.objects.filter(gender="female",sub_category='martinluther')
        context={
            'data':data,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)
    else:
        data = product_seller.objects.filter(gender="female",sub_category='Shivaji')
        context={
                'data':data,
            }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)

def filter_products_collection(request, data=None):
    price = request.GET.get('price')
    sub_category=request.GET.get('sub_category')
    
    if price=='lowtohigh' and sub_category=='Shivaji':
        products = product_seller.objects.filter(sub_category='Shivaji')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request, 'categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html',context)
    if price=='lowtohigh' and sub_category=='Babasaheb':
        products = product_seller.objects.filter(sub_category='Babasaheb')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
    if price=='lowtohigh' and sub_category=='abdulkalam':
        products = product_seller.objects.filter(sub_category='abdulkalam')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
    if price=='lowtohigh' and sub_category=='bhagatsingh':
        products = product_seller.objects.filter(sub_category='bhagatsingh')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
    if price=='lowtohigh' and sub_category=='gurunanak':
        products = product_seller.objects.filter(sub_category='gurunanak')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
    if price=='lowtohigh' and sub_category=='osho':
        products = product_seller.objects.filter(sub_category='osho')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
    if price=='lowtohigh' and sub_category=='savitribaiphule':
        products = product_seller.objects.filter(sub_category='savitribaiphule')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
    if price=='lowtohigh' and sub_category=='birsamunda':
        products = product_seller.objects.filter(sub_category='birsamunda')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
    if price=='lowtohigh' and sub_category=='buddha':
        products = product_seller.objects.filter(sub_category='buddha')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
    if price=='lowtohigh' and sub_category=='santkabir':
        products = product_seller.objects.filter(sub_category='santkabir')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
    if price=='lowtohigh' and sub_category=='martinluther':
        products = product_seller.objects.filter(sub_category='martinluther')    
        if data == 'low_to_high':
            products = products.order_by('selling_price')
        elif data == 'price_high_to_low':
            products = products.order_by('-selling_price')        
        context={
            'data': products        
        }        
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)




def filter_product_price(request,data=None):
    sub_category=request.GET.get('sub_category') 
    print('ww',sub_category)
    
    if  sub_category=='Shivaji':
        products = product_seller.objects.filter(sub_category='Shivaji')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
    elif  sub_category=='martinluther':
        products = product_seller.objects.filter(sub_category='martinluther')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)
    elif  sub_category=='Babasaheb':
        products = product_seller.objects.filter(sub_category='Babasaheb')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
    elif  sub_category=='abdulkalam':
        products = product_seller.objects.filter(sub_category='abdulkalam')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
    elif  sub_category=='bhagatsingh':
        products = product_seller.objects.filter(sub_category='bhagatsingh')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
    elif  sub_category=='gurunanak':
        products = product_seller.objects.filter(sub_category='gurunanak')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
    elif  sub_category=='osho':
        products = product_seller.objects.filter(sub_category='osho')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
    elif  sub_category=='savitribaiphule':
        products = product_seller.objects.filter(sub_category='savitribaiphule')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
    elif  sub_category=='birsamunda':
        products = product_seller.objects.filter(sub_category='birsamunda')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
    elif  sub_category=='buddha':
        products = product_seller.objects.filter(sub_category='buddha')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
    elif  sub_category=='santkabir':
        products = product_seller.objects.filter(sub_category='santkabir')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
    else:
        products = product_seller.objects.filter(sub_category='Shivaji')    
        if data == '100_500':
            products = products.filter(selling_price__range=(100, 500))
        elif data == '500_1000':
            products = products.filter(selling_price__range=(500, 1000))
        elif data == 'above_1000':
            products = products.filter(selling_price__gte=1000)
        context={
            'data':products,
        }
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)



def filter_colour_collection(request,data):
    selected_colors = request.GET.getlist('colour')
    sub_category=request.GET.get('sub_category') 
    pro_data = product_seller.objects.all()  
    products=[]
    if data=='Shivaji':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='Shivaji') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
    if data=='Babasaheb':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='Babasaheb') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
    if data=='abdulkalam':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='abdulkalam') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
    if data=='bhagatsingh':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='bhagatsingh') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
    if data=='gurunanak':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='gurunanak') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
    if data=='osho':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='osho') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
    if data=='savitribaiphule':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='savitribaiphule') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
    if data=='birsamunda':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='birsamunda') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
    if data=='buddha':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='buddha') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
    if data=='santkabir':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='santkabir') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
    if data=='martinluther':
        if selected_colors:
            filtered_products = pro_data.filter(colour__in=selected_colors,sub_category='martinluther') 
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)


def filter_size_collection(request,data):
    pro_data = product_seller.objects.all()  
    selected_size = request.GET.getlist('size')
    
    if data=='Shivaji':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='Shivaji'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
    elif data=='Babasaheb':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='Babasaheb'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
    elif data=='abdulkalam':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='abdulkalam'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
    elif data=='bhagatsingh':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='bhagatsingh'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
    elif data=='gurunanak':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='gurunanak'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
    elif data=='osho':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='osho'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
    elif data=='savitribaiphule':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='savitribaiphule'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
    elif data=='birsamunda':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='birsamunda'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
    elif data=='buddha':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='buddha'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
    elif data=='santkabir':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='santkabir'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
    elif data=='martinluther':
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='martinluther'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)
    else:
        if selected_size:
            filtered_products = []
            for size in selected_size:                
                filtered_products.extend(pro_data.filter(size__iexact=size,sub_category='Shivaji'))
            products = filtered_products
        context = {
                'data': products,
            }    
        return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)


from datetime import datetime, time
from datetime import datetime, timedelta

def updated_products(request):
    current_datetime = datetime.now()
    start_date = current_datetime - timedelta(days=10)
    sub_category=request.GET.get('sub_category')
    if sub_category=='Shivaji':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='Shivaji')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html")

    elif sub_category=='Babasaheb':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='Babasaheb')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/BRAmbedkar-quotes.html")
    elif sub_category=='abdulkalam':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='abdulkalam')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/A.PJAbdulKalam-quotes.html")
    elif sub_category=='bhagatsingh':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='bhagatsingh')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Bhagatsingh-quotes.html")
    elif sub_category=='gurunanak':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='gurunanak')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Gurunanak-quotes.html")
    elif sub_category=='osho':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='osho')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/osho-quotes.html")
    elif sub_category=='savitribaiphule':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='savitribaiphule')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Savitribaifule-quotes.html")
    elif sub_category=='birsamunda':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='birsamunda')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Birsamunda-quotes.html")
    elif sub_category=='buddha':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='buddha')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/budhha-quotes.html")
    elif sub_category=='santkabir':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='santkabir')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Santkabir-quotes.html")
    elif sub_category=='martinluther':        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='martinluther')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/MartinLutherKing-quotes.html")
    else:        
        products = product_seller.objects.filter(product_type="T-shirt", product_date__range=(start_date, current_datetime),sub_category='Shivaji')
        context={
            'data':products
            }   
        if products:     
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html",context)
        else:
            return render(request,"categories/clothing-category/t-shirts-and-shirts/quotes-category/Shivajimaharaj-quotes.html")


      
from django.db.models import Q
def search(request):
    query = request.GET.get('search')
    Category = request.GET.get('category')
    data = None

    if query:
        # Start with a base query
        data = product_seller.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(product_type__icontains=query) |
            Q(brand__icontains=query)
        )
    data1 = product_seller.objects.filter(category__icontains=Category)
    print('ccccccccccccccccccccccccccccccccccccc',Category)
    print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',query)
    print('ddddddddddddddddddddddddddddddddddddd',data1)
    return render(request, 'search/search_results.html', {'results': data, 'query': query, 'category': data1})










import requests
from django.http import JsonResponse
from django.shortcuts import render

# def create_order_api(request):
    
#     first_name = request.GET.get('first_name')
#     last_name = request.GET.get('last_name')  # Use the default date if "dob" is not provided
#     mobile_no = request.GET.get('mobile_no')
#     custom_order_id = request.GET.get(1234)
#     vendor_id= request.GET.get(40109)
#     device_from = request.GET.get(4)
#     product_name= request.GET.get('product_name')
#     price = request.GET.get('price')
#     old_price = request.GET.get('old_price')
    
#     email= request.GET.get('email')
#     address= request.GET.get('address')
#     state= request.GET.get( 'state')
#     city= request.GET.get( 'city')
#     zip_code= request.GET.get( 'zip_code')
#     landmark= request.GET.get( 'landmark')
#     payment_method= request.GET.get(4)
#     qty= request.GET.get('qty')
    

#     url = "https://selloship.com/web_api/Create_order"
#     files=[

#     ]
#     headers = {
#         'Authorization': 'bd953055261075e00e73c55f4941fe186a95809153bea8d1903650f',
#         'Cookie': 'AWSALB=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; AWSALBCORS=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; ci_session=pqh3eqv8k7o4ruvmc4b1bvqbhv66arjv'
#     }

#     try:
#         response = requests.get(url,  headers=headers, files=files)

#         if response.status_code == 200:
#             data = response.json()
#             # Print the entire JSON response for debugging
#             print("666666666666666",data)
#             context = {
#                 'data': data,
#                 'error': None,
#             }
#             return render(request, 'customer/tracking.html/', context)
#         else:
#             return JsonResponse({'error': 'Failed to retrieve data'}, status=500)
#     except Exception as e:
#         # Print the exception for debugging
#         print(e)
#         return JsonResponse({'error': 'An error occurred'}, status=500)



import requests
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render

import requests
import random
import string

# def create_order_api(request):
#     # Your existing code

    
#     # Make the API request to login and get the access token
#     login_url = "https://selloship.com/api/lock_actvs/Vendor_login_from_vendor_all_order"
#     login_payload = {'email': 'sanjog.meshram@gmail.com', 'password': 'Kanu@0507'}
#     login_headers = {'Authorization': '9f3017fd5aa17086b98e5305d64c232168052b46c77a3cc16a5067b'}
    
#     try:
#         login_response = requests.post(login_url, headers=login_headers, data=login_payload)
#         login_data = login_response.json()
#         print("login_data",login_data)
        
#         if login_data.get('success') == '1':
#             vendor_id = login_data.get('vendor_id')
#             print("0000000",vendor_id)
#             access_token = login_data.get('access_token')
#             device_from = login_data.get('device_from')
#             print("0000000",vendor_id,device_from,access_token)
            
#             # Use the retrieved data in your API request for creating an order
#             url = "https://selloship.com/web_api/Create_order"
#             headers = {
#                 'Authorization': access_token,
#                 'Cookie': 'AWSALB=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; AWSALBCORS=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; ci_session=pqh3eqv8k7o4ruvmc4b1bvqbhv66arjv'
#             }
            
#             # Include your order creation payload and files as needed
#             print(request.user.email)
            
            
#             data1 = customer_user.objects.filter(email=request.user.email).values('first_name','last_name','mobile_number','email','locality', 'city','pincode','state')
#             print("data1",data1)
#             payload = {
#                 'vendor_id': vendor_id,
#                 'device_from': device_from,
#                 # Add other necessary fields for creating the order
#                 'data1':data1,
#                 'payment_method':3,
#                 'address':'katol naka'
#                 'product_name':'tshirt',
#                 'price':23400,
#                 'old_price':2344,
#                 'qty':1,
#                 'customer_order_id':2000,
                
#             }
#             print("0000000000",payload)
#             files = []
            
#             try:
#                 order_response = requests.post(url, headers=headers, data=payload, files=files)
#                 print("order_response response:", order_response)
                
#                 if order_response.status_code == 200:
#                     contain = order_response.json()
#                     # Print or process the response as needed
#                     print("Order creation response:", contain)
#                     context = {
#                         'data': contain,
#                         'error': None,
#                     }
                
#                     return render(request, 'customer/tracking.html/', context)
#                 else:
#                     return JsonResponse({'error': 'Failed to create order'}, status=order_response.status_code)
#             except Exception as e:
#                 # Handle exceptions when making the order creation request
#                 print("Error creating order:", e)
#                 return JsonResponse({'error': 'An error occurred while creating order'}, status=500)
#         else:
#             return JsonResponse({'error': 'Login failed'}, status=401)
#     except Exception as e:
#         # Handle exceptions when making the login request
#         print("Error logging in:", e)
#         return JsonResponse({'error': 'An error occurred while logging in'}, status=500)




def create_order_api(request):
    # Your existing code
    total_amount = request.GET.get('total_amount')
    custid = request.GET.get('custid')
    user = request.user
    pay = request.GET.get('COD')
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

        price = Decimal(product.discount_price)
        product_price = Decimal(product.selling_price) * cart_item.quantity
        tax = product_price * Decimal('0.18')
        total_cost = product_price + tax + Decimal('50')
        
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
            tax=tax,
            product_price=product_price,
            total_cost=total_cost,
        )

        product.quantity = F('quantity') - cart_item.quantity
        product.save()  
        cart_item.delete()

    data = OrderPlaced.objects.filter(user=user, order_id=order_id)
   
    mrpamount = sum(Decimal(p.quantity) * Decimal(p.product.selling_price) for p in cart_items)
    tax = (mrpamount * Decimal('0.18'))
    ship = Decimal('50')
    totalamount = mrpamount + tax + ship
    grand_total = totalamount
    ship_charge1 = 50
    total_amount_float = float(total_amount)
    ship_charge = str(50)
    total_data = total_amount_float + ship_charge1
    
    for item in data:
        item.total_cost = total_data
        item.save()

    subject = 'Purchase Confirmation from Vishwaratna.'
    message = "\n Thank you for your purchase on Vishwaratna! We are delighted to confirm that your order has been successfully processed.\nWe appreciate your trust in us for your shopping needs. If you have any questions or need further assistance, please don't hesitate to contact us.\nThank you for choosing Vishwaratna for your shopping experience!\n\nBest regards,\nVR Team. "
    from_email = "vishwaratnasite@gmail.com"
    recipient_list = [cust.user.email]

    customer_name = f"{cust.first_name} {cust.last_name}"
    customer_address = f"{cust.locality}, {cust.city}, {cust.pincode}, {cust.state}"

    product_details = []
    for cart_item in cart_items:
        product_name = cart_item.product.title
        quantity = cart_item.quantity
        order_amount = total_amount
        product_details.append(f"{product_name}: {quantity}")
        
    payment_method = pay
    invoice_number = invoice_id

    admin_email = 'vishwaratnasite@gmail.com'
    admin_subject = 'New Order Placed From Customer'
    admin_message = f"New Order Placed:\n\nOrder Amount: {order_amount}\nCustomer Name: {customer_name}\nCustomer Address: {customer_address}\n\nProduct Details:\n"
    admin_message += "\n".join(product_details)
    admin_message += f"\n\nPayment Method: {payment_method}\nInvoice Number: {invoice_number}"

    email_context = {
        'order_items': data,
        'order_total': total_amount,
        'order_tax': tax,
        'order_shipping': ship,
        'order_grand_total': total_amount,
    }
    discount_on_mrp = 0
    context = {
        'grand_total1': total_data,
        'tax': tax,
        'totalamount': totalamount,
        'data': data,
        'cust': cust,
        'order_id': order_id,
        'cart': cart_items,
        'mrpamount': mrpamount, 
        'price':price,
        'discount_on_mrp':discount_on_mrp,
        'pay':pay
    }
    product_name = f"{order.product}, Size:{order.size}"
    print("99999999999",product_name)
    
    # Make the API request to login and get the access token
    login_url = "https://selloship.com/api/lock_actvs/Vendor_login_from_vendor_all_order"
    login_payload = {'email': 'sanjog.meshram@gmail.com', 'password': 'Kanu@0507'}
    login_headers = {'Authorization': '9f3017fd5aa17086b98e5305d64c232168052b46c77a3cc16a5067b'}
    
    try:
        login_response = requests.post(login_url, headers=login_headers, data=login_payload)
        login_data = login_response.json()
        print("login_data", login_data)
        
        if login_data.get('success') == '1':
            vendor_id = login_data.get('vendor_id')
            access_token = login_data.get('access_token')
            device_from = login_data.get('device_from')
            
            # Check if the order creation API response is successful
            order_url = "https://selloship.com/web_api/Create_order"
            order_payload = {
                'vendor_id': vendor_id,
                'device_from': device_from,
                'product_name': product_name,
                'price': str(totalamount),
                'old_price': str(total_cost),
                'first_name': cust.first_name,
                'last_name': cust.last_name,
                'mobile_no': cust.mobile_number,
                'email': cust.user.email,
                'address': cust.locality,
                'state': cust.state,
                'city': cust.city,
                'zip_code': cust.pincode,
                
                'payment_method': pay,
                'qty': order.quantity,
                'custom_order_id': order.order_id,
            }
            print("0000000000000000000000000",order_payload)
            order_headers = {'Authorization': access_token, 'Cookie': 'AWSALB=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; AWSALBCORS=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; ci_session=pqh3eqv8k7o4ruvmc4b1bvqbhv66arjv'}
            
            try:
                order_response = requests.post(order_url, headers=order_headers, data=order_payload)
                print("order_response response:", order_response.text)

                data = OrderPlaced.objects.filter(user=user, order_id=order_id)
                if order_response.status_code == 200:
                    order_data = order_response.json()
                    if order_data.get('success') == '1':
                        selloship_order_id = order_data.get('selloship_order_id')
                        selloship_url = order_data.get('selloship_url')
                        print("11111",selloship_url,selloship_order_id,order)
                        
                        order.selloship_id = selloship_order_id  # Replace your_order_id with the actual order ID

                        # Update the selloship_order_id field
                        
                        order.save()
                        print("mmmmmmmmmmmmm",order)
                        
                        # Use the order data as needed, for example, redirect to the order view URL
                        return render(request, "customer/order_success.html",context)
                    else:
                        return JsonResponse({'error': 'Order creation failed'}, status=500)
                else:
                    return JsonResponse({'error': 'Failed to create order'}, status=order_response.status_code)
            except Exception as e:
                print("Error creating order:", e)
                return JsonResponse({'error': 'An error occurred while creating order'}, status=500)
        else:
            return JsonResponse({'error': 'Login failed'}, status=401)
    except Exception as e:
        print("Error logging in:", e)
        return JsonResponse({'error': 'An error occurred while logging in'}, status=500)







def cancel_order_api(request,order_id):
    # Your existing code
    try:
        order = OrderPlaced.objects.get(order_id=order_id)
    except OrderPlaced.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    print('bbbbbbbbbb',order.payment_method)
    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason')

        if order.payment_method =="Razorpay":
                # Initialize Razorpay client
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Fetch the payment ID associated with the order
            payment_id = order.razorpay_payment_id

            user=request.user
            
            try:
                # Initiate refund for the payment
                refund_response = razorpay_client.payment.refund(payment_id, { 'amount': int(float(order.total_cost) * 100) })
                # Check refund status
                if refund_response['status'] == 'processed':
                    # Refund successful, proceed with canceling the order
                    order.canceled = True
                    order.cancel_reason = cancel_reason
                    order.save()

                    # Create a record of the canceled order
                    CanceledOrder.objects.create(
                        order_id=order.order_id,
                        customer=order.customer,
                        product=order.product,
                        quantity=order.quantity,
                        canceled_reason=cancel_reason,
                        payment_method=order.payment_method,
                        invoice_no=order.invoice_no,
                        total_cost=order.total_cost,
                        razorpay_order_id=order.razorpay_order_id,
                        razorpay_payment_id=order.razorpay_payment_id 
                    )

                    # Remove the order from the main list of orders
                    
                    order.delete()
                    
                    subject = 'cancel orders payment Refund .'
                    message = "\n Cancel orders Payment Refunded to your account.\nBest regards,\nVR Team. "
                    from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


                    return redirect('/orders/')
                else:
                    # Refund failed, handle the error
                    return HttpResponse("Refund failed", status=500)  # You can customize this error response as needed
                
            except Exception as e:
                # Handle exceptions
                return HttpResponse("Refund failed: " + str(e), status=500)  # You can customize this error response as needed
        else:
            order.canceled = True
            order.cancel_reason = cancel_reason
            order.save()
            print("99999999999999",order.cancel_reason)

            # Create a record of the canceled order
            CanceledOrder.objects.create(
                order_id=order.order_id,
                customer=order.customer,
                product=order.product,
                quantity=order.quantity,
                canceled_reason=cancel_reason,
                payment_method=order.payment_method,
                invoice_no=order.invoice_no,
                total_cost=order.total_cost 
            )


            # Remove the order from the main list of orders
            order.delete()
            return redirect('/orders/')
            
    
    # Make the API request to login and get the access token
    login_url = "https://selloship.com/api/lock_actvs/Vendor_login_from_vendor_all_order"
    login_payload = {'email': 'sanjog.meshram@gmail.com', 'password': 'Kanu@0507'}
    login_headers = {'Authorization': '9f3017fd5aa17086b98e5305d64c232168052b46c77a3cc16a5067b'}
    
    try:
        login_response = requests.post(login_url, headers=login_headers, data=login_payload)
        login_data = login_response.json()
        print("login_data",login_data)
        
        if login_data.get('success') == '1':
            vendor_id = login_data.get('vendor_id')
            print("0000000",vendor_id)
            access_token = login_data.get('access_token')
            device_from = login_data.get('device_from')
            print("0000000",vendor_id,device_from,access_token)
            
            # Use the retrieved data in your API request for creating an order
            url =  "https://selloship.com/api/lock_actvs/Vendor_cancel_order"
            headers = {
                'Authorization': access_token,
                'Cookie': 'AWSALB=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; AWSALBCORS=2z8HrwoTfLC2IlolC4Y+rmU0IUgabIziAFQo78uqzE0qBCju0e8CC+aIwb3/mjANyC4dqhP4XGXYIPYLtbe1cUPPjJZBjdW8b7cr+YV1E9XeeKQhOvi5VObjWhe1; ci_session=pqh3eqv8k7o4ruvmc4b1bvqbhv66arjv'
            }
            
            # Include your order creation payload and files as needed
            print(request.user.email)
            
            
            payload = {
                'vendor_id': '40109',
                'device_from': '4',
                'order_id': order.selloship_id,
                'cancel_note': order.cancel_reason,
            }
            
            print("0000000000",payload)
            files = []
            
            try:
                order_response = requests.post(url, headers=headers, data=payload, files=files)
                print("order_response response:", order_response)
                
                if order_response.status_code == 200:
                    contain = order_response.json()
                    # Print or process the response as needed
                    print("Order creation response:", contain)
                    context = {
                        'data': contain,
                        'error': None,
                        'order': order,
                    }
                
                    
                    return render(request, "customer/cancel_orders.html", context)

                else:
                    return JsonResponse({'error': 'Failed to create order'}, status=order_response.status_code)
            except Exception as e:
                # Handle exceptions when making the order creation request
                print("Error creating order:", e)
                return JsonResponse({'error': 'An error occurred while creating order'}, status=500)
        else:
            return JsonResponse({'error': 'Login failed'}, status=401)
    except Exception as e:
        # Handle exceptions when making the login request
        print("Error logging in:", e)
        return JsonResponse({'error': 'An error occurred while logging in'}, status=500)

