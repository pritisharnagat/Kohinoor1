
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect
from Admin.models import * 
from django.template import loader
from django.http import HttpResponse, JsonResponse
from customer.models import *
from django.db.models import Avg
# Create your views here.
from django.db.models import Count
from decimal import Decimal, ROUND_HALF_UP

from customer.models import *
from collections import defaultdict

def navbar(request):
    all_data = product_seller.objects.filter(product_approved=True)[:4]
    all_product = product_seller.objects.all()
    data1=product_seller.objects.filter(sub_category="Shivaji")[:4]
    latest_entries = product_seller.objects.filter(sub_category="Babasaheb").order_by('-id')[:4]
    data3 = product_seller.objects.filter(sub_category="abdulkalam").order_by('-id')[:4]
    data4 = product_seller.objects.filter(sub_category="bhagatsingh").order_by('-id')[:4]
    data5 = product_seller.objects.filter(sub_category="gurunanak").order_by('-id')[:4]
    data6 = product_seller.objects.filter(sub_category="osho").order_by('-id')[:4]
    data7 = product_seller.objects.filter(sub_category="savitribaiphule").order_by('-id')[:4]
    data8 = product_seller.objects.filter(sub_category="birsamunda").order_by('-id')[:4]
    data9 = product_seller.objects.filter(sub_category="buddha").order_by('-id')[:4]
    data10 = product_seller.objects.filter(sub_category="santkabir").order_by('-id')[:4]
    data11 = product_seller.objects.filter(sub_category="martinluther").order_by('-id')[:4]


    context={
    'all_data':all_data,
    'all_product':all_product,
    'data1':data1,
    'data2':latest_entries,
    'data3':data3,
    'data4':data4,
    'data5':data5,
    'data6':data6,
    'data7':data7,
    'data8':data8,
    'data9':data9,
    'data10':data10,
    'data11':data11,
    }
    return render(request,'landing_page.html',context)

def home(request):
    all_product_sellers = product_seller.objects.all()

    # Filter product_seller entries by sub_category and get the first entry for each unique product_id
    filtered_product_sellers = []
    seen_product_ids = set()

    for seller in all_product_sellers.filter(sub_category="Shivaji"):
        if seller.product_id not in seen_product_ids:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_product_sellers.append(seller)
            seen_product_ids.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data1 = filtered_product_sellers[:4]

    filtered_Babasaheb = []
    seen_product_babasaheb = set()

    for seller in all_product_sellers.filter(sub_category="Babasaheb"):
        if seller.product_id not in seen_product_babasaheb:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_Babasaheb.append(seller)
            seen_product_babasaheb.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    latest_entries = filtered_Babasaheb[:4]


    filtered_abdulkalam = []
    seen_product_abdulkalam = set()

    for seller in all_product_sellers.filter(sub_category="abdulkalam"):
        if seller.product_id not in seen_product_abdulkalam:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_abdulkalam.append(seller)
            seen_product_abdulkalam.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data3 = filtered_abdulkalam[:4]


    filtered_bhagatsingh = []
    seen_product_bhagatsingh = set()

    for seller in all_product_sellers.filter(sub_category="bhagatsingh"):
        if seller.product_id not in seen_product_bhagatsingh:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_bhagatsingh.append(seller)
            seen_product_bhagatsingh.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data4 = filtered_bhagatsingh[:4]


    filtered_gurunanak = []
    seen_product_gurunanak = set()

    for seller in all_product_sellers.filter(sub_category="gurunanak"):
        if seller.product_id not in seen_product_gurunanak:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_gurunanak.append(seller)
            seen_product_gurunanak.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data5 = filtered_gurunanak[:4]


    filtered_osho = []
    seen_product_osho = set()

    for seller in all_product_sellers.filter(sub_category="osho"):
        if seller.product_id not in seen_product_osho:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_osho.append(seller)
            seen_product_osho.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data6 = filtered_osho[:4]


    filtered_savitribaiphule = []
    seen_product_savitribaiphule = set()

    for seller in all_product_sellers.filter(sub_category="savitribaiphule"):
        if seller.product_id not in seen_product_savitribaiphule:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_savitribaiphule.append(seller)
            seen_product_savitribaiphule.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data7 = filtered_savitribaiphule[:4]

    filtered_birsamunda = []
    seen_product_birsamunda = set()

    for seller in all_product_sellers.filter(sub_category="birsamunda"):
        if seller.product_id not in seen_product_birsamunda:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_birsamunda.append(seller)
            seen_product_birsamunda.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data8 = filtered_birsamunda[:4]


    filtered_buddha = []
    seen_product_buddha = set()

    for seller in all_product_sellers.filter(sub_category="buddha"):
        if seller.product_id not in seen_product_buddha:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_buddha.append(seller)
            seen_product_buddha.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data9 = filtered_buddha[:4]


    filtered_santkabir = []
    seen_product_santkabir = set()

    for seller in all_product_sellers.filter(sub_category="santkabir"):
        if seller.product_id not in seen_product_santkabir:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_santkabir.append(seller)
            seen_product_santkabir.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data10 = filtered_santkabir[:4]


    filtered_martinluther = []
    seen_product_martinluther = set()

    for seller in all_product_sellers.filter(sub_category="martinluther"):
        if seller.product_id not in seen_product_martinluther:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_martinluther.append(seller)
            seen_product_martinluther.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data11 = filtered_martinluther[:4]
    


    # Filter the latest entries by sub_category
    # data2 = latest_entries.filter(sub_category="Babasaheb")

    all_data = product_seller.objects.filter(product_approved=True)[:4]
    all_product = product_seller.objects.all()
    # data1=product_seller.objects.filter(sub_category="Shivaji")[:4]
    # latest_entries = product_seller.objects.filter(sub_category="Babasaheb").order_by('-id')[:4]
    # data3 = product_seller.objects.filter(sub_category="abdulkalam").order_by('-id')[:4]
    # data4 = product_seller.objects.filter(sub_category="bhagatsingh").order_by('-id')[:4]
    # data5 = product_seller.objects.filter(sub_category="gurunanak").order_by('-id')[:4]
    # data6 = product_seller.objects.filter(sub_category="osho").order_by('-id')[:4]
    # data7 = product_seller.objects.filter(sub_category="savitribaiphule").order_by('-id')[:4]
    # data8 = product_seller.objects.filter(sub_category="birsamunda").order_by('-id')[:4]
    # data9 = product_seller.objects.filter(sub_category="buddha").order_by('-id')[:4]
    # data10 = product_seller.objects.filter(sub_category="santkabir").order_by('-id')[:4]
    # data11 = product_seller.objects.filter(sub_category="martinluther").order_by('-id')[:4]

    avg_rating = Customer_Review.objects.all()
    # print('fffffffffffffffffff',avg_rating)

    product_ids = list(all_product.values_list('prod_id', flat=True))
    # print('product_ids',product_ids)

    # Customer_Review model to calculate average ratings
    product_ratings = {}
    for product_id in product_ids:
        # print('aparna',product_id)
        reviews = Customer_Review.objects.filter(product__prod_id=product_id)
        # print('reviewsreviews',reviews)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('review_star'))['review_star__avg']
            if average_rating is not None:
                # Round average_rating to one decimal place
                rounded_rating = Decimal(average_rating).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
                product_ratings[product_id] = rounded_rating
                # print('rounded_rating',rounded_rating)
            else:
                product_ratings[product_id] = None  # No reviews found for this product
        else:
            product_ratings[product_id] = None

        # if reviews.exists():
        #     average_rating = reviews.aggregate(Avg('review_star'))['review_star__avg']
        #     product_ratings[product_id] = average_rating
        # else:
        #     product_ratings[product_id] = None  # No reviews found for this product

    # Example: Updating average_rating field in product_seller instances
    for product in all_product:
        prod_id = product.prod_id
        # print('aparna search',prod_id)
        if prod_id in product_ratings and product_ratings[prod_id] is not None:
            product.average_rating = product_ratings[prod_id]
            product.save()
        else:
            product.average_rating = None  # No reviews found
            product.save()

    events = Event.objects.all()
    event_discount = Event.objects.filter(event_date=datetime.now().date()).values('event_discount', 'event_name')
    
    for event in event_discount:
       event['event_discount'] *= 100
    
    count = ''  
    if request.user.is_authenticated:
        user = request.user.username
        data = Wishlist.objects.filter(user__username = user).order_by('-id')
        
        count = data.count()

    context={
    'all_data':all_data,
    'all_product':all_product,
    'data1':data1,
    'data2':latest_entries,
    'data3':data3,
    'data4':data4,
    'data5':data5,
    'data6':data6,
    'data7':data7,
    'data8':data8,
    'data9':data9,
    'data10':data10,
    'data11':data11,
    'event_discount':event_discount,
    'count':count,
    }
    return render(request,'page1.html',context)


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        # Save the email to your database (replace SubscribedEmail with your actual model)
        SubscribedEmail.objects.create(email=email)

        # You can redirect to the home page or any other page after successful subscription
        return redirect('home')
    
    # Handle GET requests or any other logic as needed
    return render(request, 'landing_page.html')



def cust_registeration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if VrUser.objects.filter(email=email).exists():
            # If user already exists, you can handle this case accordingly
            return render(request,'login/customer_register.html',{'error_message': 'User with this email already exists.'})
            # return render(request, 'login/registration_error.html', {'error_message': 'User with this email already exists.'})
        if VrUser.objects.filter(mobile_number=mobile_number).exists():
            # If user already exists, you can handle this case accordingly
            return render(request,'login/customer_register.html',{'error_message1': 'User with this contact number already exists.'})
        
        mydata = VrUser(first_name=first_name, last_name=last_name, email=email, username=email, mobile_number=mobile_number,is_Vruser=True,is_customer=True,is_active=True)
        mydata.set_password(password)
        mydata.save()
        
        customer_profile = customer_user(user=mydata, first_name=first_name, last_name=last_name, email=email, mobile_number=mobile_number, is_customer=True,is_active=True)
        customer_profile.save()

        subject = "Welcome to Vibetara - Complete Your Registration!"
        message = f"Hi {mydata.first_name},\n\n"
        message += "Welcome to Vibetara!\n\n"
        message += "We're thrilled to have you join our community of shoppers. To complete your registration and start exploring the latest trends in fashion, and more, simply click on the link below:\n"
        registration_link = "http://vibetara.com/customer_register/"
        message += f"{registration_link}\n\n"
        message += "Once again, welcome aboard, and happy shopping!\n\n"
        message += "Best regards,\nThe Vibetara Team"
        from_email = "vishwaratnasite@gmail.com"  # Replace this with your desired 'from' email address
        recipient_list = [mydata.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('/customer_login/')
    return render(request,'login/customer_register.html')


def cust_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        VrUser = authenticate(email=email, password=password)
        print("userr",VrUser)

        if VrUser is not None and VrUser.is_customer:
            # Log in the user
            login(request,VrUser)
            
            return redirect('/customer_after_login/')  
        else:
           
            error_message = "Invalid login credentials. Please try again."
            messages.error(request, error_message)
            # return render(request, 'registeration/customer_register.html', {'error_message': error_message})

    return render(request, 'login/customer_login.html')


# @login_required(login_url='/customer_login/')
# def customer_after_login(request):
#     user = customer_user.objects.get(email=request.user.email)
#     all_data = product_seller.objects.filter(product_approved=True)
#     latest_entries = product_seller.objects.filter(sub_category="Babasaheb").order_by('-id')[:4]
#     data1=product_seller.objects.filter(sub_category="Shivaji")[:4]
#     data3 = product_seller.objects.filter(sub_category="abdulkalam").order_by('-id')[:4]
#     data4 = product_seller.objects.filter(sub_category="bhagatsingh").order_by('-id')[:4]
#     data5 = product_seller.objects.filter(sub_category="gurunanak").order_by('-id')[:4]
#     data6 = product_seller.objects.filter(sub_category="osho").order_by('-id')[:4]
#     data7 = product_seller.objects.filter(sub_category="savitribaiphule").order_by('-id')[:4]
#     data8 = product_seller.objects.filter(sub_category="birsamunda").order_by('-id')[:4]
#     data9 = product_seller.objects.filter(sub_category="buddha").order_by('-id')[:4]
#     data10 = product_seller.objects.filter(sub_category="santkabir").order_by('-id')[:4]
#     data11 = product_seller.objects.filter(sub_category="martinluther").order_by('-id')[:4]

#     for product in all_data:
#         average_rating = Customer_Review.objects.filter(product=product).aggregate(Avg('review_star'))['review_star__avg']
#         print('999999999999999999999999999999999999',average_rating)

#         if average_rating is not None:
#             average_rating = round(average_rating)
#         else:
#             average_rating = None

#         product.average_rating = average_rating

#     # user = customer_user.objects.get(email=request.user.email)
#     user1 = request.user

#     all_blog = BlogPost.objects.all()
    
#     for i in all_blog:
#         print('fffffffffffffffffff',i.image1,i.image2)

#     all_product = product_seller.objects.all()

#     for product in all_product:
#         average_rating = Customer_Review.objects.filter(product=product).aggregate(Avg('review_star'))['review_star__avg']
#         print('999999999999999999999999999999999999',average_rating)

#         if average_rating is not None:
#             average_rating = round(average_rating)
#         else:
#             average_rating = None

#         product.average_rating = average_rating

#     events = Event.objects.all()
#     event_discount = Event.objects.filter(event_date=datetime.now().date()).values('event_discount', 'event_name')
    
#     for event in event_discount:
#        event['event_discount'] *= 100


#     data = Wishlist.objects.filter(user = user1)
#     count = data.count()
#     print('sssssssssssssss',data)
   
#     context={
#     'all_data':all_data,
#     # 'user':user,
#     'count':count,
#     'all_blog':all_blog,
#     'all_product':all_product,
#     'data2':latest_entries,
#     'data1':data1,
#     'data3':data3,
#     'data4':data4,
#     'data5':data5,
#     'data6':data6,
#     'data7':data7,
#     'data8':data8,
#     'data9':data9,
#     'data10':data10,
#     'data11':data11,
#     'user':user,
#     'event_discount':event_discount,
   
#     }

#     return render(request, "customer_base.html", context)

from django.core.mail import send_mail
from django.conf import settings       
def send_cart_reminder_email(user_email):
    cart_url = reverse('view_cart')  # Get the URL for the cart page

    subject = "Don't Miss Out on Your Favorites at Vibetara!"
    message = """
    Dear Customer,
    
    We noticed that you've added some items to your cart on Vibetara but haven't completed your purchase yet. Your selected items are eagerly waiting for you!
    
    Remember, our products are selling out fast, and we wouldn't want you to miss out on your favorites. Plus, with our secure checkout process, you can shop with confidence.
    
    Go to  your cart and complete your purchase.
    
    Thank you for considering Vibetara for your shopping needs. Should you have any questions or require assistance, please don't hesitate to contact our customer support team.
    
    Happy shopping!
    
    Best regards,
    The Vibetara Team
    """

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


@login_required(login_url='/customer_login/')
def customer_after_login(request):
    user = customer_user.objects.get(email=request.user.email)
    user_email = request.user.email
    send_cart_reminder_email(user_email)  # Send cart reminder email
    
    all_product_sellers = product_seller.objects.all()
    user = customer_user.objects.get(email=request.user.email)
    # Filter product_seller entries by sub_category and get the first entry for each unique product_id
    filtered_product_sellers = []
    seen_product_ids = set()

    for seller in all_product_sellers.filter(sub_category="Shivaji"):
        if seller.product_id not in seen_product_ids:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_product_sellers.append(seller)
            seen_product_ids.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data1 = filtered_product_sellers[:4]

    filtered_Babasaheb = []
    seen_product_babasaheb = set()

    for seller in all_product_sellers.filter(sub_category="Babasaheb"):
        if seller.product_id not in seen_product_babasaheb:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_Babasaheb.append(seller)
            seen_product_babasaheb.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data2 = filtered_Babasaheb[:4]


    filtered_abdulkalam = []
    seen_product_abdulkalam = set()

    for seller in all_product_sellers.filter(sub_category="abdulkalam"):
        if seller.product_id not in seen_product_abdulkalam:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_abdulkalam.append(seller)
            seen_product_abdulkalam.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data3 = filtered_abdulkalam[:4]


    filtered_bhagatsingh = []
    seen_product_bhagatsingh = set()

    for seller in all_product_sellers.filter(sub_category="bhagatsingh"):
        if seller.product_id not in seen_product_bhagatsingh:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_bhagatsingh.append(seller)
            seen_product_bhagatsingh.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data4 = filtered_bhagatsingh[:4]


    filtered_gurunanak = []
    seen_product_gurunanak = set()

    for seller in all_product_sellers.filter(sub_category="gurunanak"):
        if seller.product_id not in seen_product_gurunanak:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_gurunanak.append(seller)
            seen_product_gurunanak.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data5 = filtered_gurunanak[:4]


    filtered_osho = []
    seen_product_osho = set()

    for seller in all_product_sellers.filter(sub_category="osho"):
        if seller.product_id not in seen_product_osho:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_osho.append(seller)
            seen_product_osho.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data6 = filtered_osho[:4]


    filtered_savitribaiphule = []
    seen_product_savitribaiphule = set()

    for seller in all_product_sellers.filter(sub_category="savitribaiphule"):
        if seller.product_id not in seen_product_savitribaiphule:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_savitribaiphule.append(seller)
            seen_product_savitribaiphule.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data7 = filtered_savitribaiphule[:4]

    filtered_birsamunda = []
    seen_product_birsamunda = set()

    for seller in all_product_sellers.filter(sub_category="birsamunda"):
        if seller.product_id not in seen_product_birsamunda:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_birsamunda.append(seller)
            seen_product_birsamunda.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data8 = filtered_birsamunda[:4]


    filtered_buddha = []
    seen_product_buddha = set()

    for seller in all_product_sellers.filter(sub_category="buddha"):
        if seller.product_id not in seen_product_buddha:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_buddha.append(seller)
            seen_product_buddha.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data9 = filtered_buddha[:4]


    filtered_santkabir = []
    seen_product_santkabir = set()

    for seller in all_product_sellers.filter(sub_category="santkabir"):
        if seller.product_id not in seen_product_santkabir:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_santkabir.append(seller)
            seen_product_santkabir.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data10 = filtered_santkabir[:4]


    filtered_martinluther = []
    seen_product_martinluther = set()

    for seller in all_product_sellers.filter(sub_category="martinluther"):
        if seller.product_id not in seen_product_martinluther:
            # Add the first entry (earliest entry) for each unique product_id
            filtered_martinluther.append(seller)
            seen_product_martinluther.add(seller.product_id)

            # If you only need the first entry for each product_id, you can break the loop here
            # Remove the break statement if you want to continue processing all entries

    # You can limit the number of results to 4, as mentioned in your example
    data11 = filtered_martinluther[:4]
    
    all_data = product_seller.objects.filter(product_approved=True)
    # latest_entries = product_seller.objects.filter(sub_category="Babasaheb").order_by('-id')[:4]
    # data1=product_seller.objects.filter(sub_category="Shivaji")[:4]
    # data3 = product_seller.objects.filter(sub_category="abdulkalam").order_by('-id')[:4]
    # data4 = product_seller.objects.filter(sub_category="bhagatsingh").order_by('-id')[:4]
    # data5 = product_seller.objects.filter(sub_category="gurunanak").order_by('-id')[:4]
    # data6 = product_seller.objects.filter(sub_category="osho").order_by('-id')[:4]
    # data7 = product_seller.objects.filter(sub_category="savitribaiphule").order_by('-id')[:4]
    # data8 = product_seller.objects.filter(sub_category="birsamunda").order_by('-id')[:4]
    # data9 = product_seller.objects.filter(sub_category="buddha").order_by('-id')[:4]
    # data10 = product_seller.objects.filter(sub_category="santkabir").order_by('-id')[:4]
    # data11 = product_seller.objects.filter(sub_category="martinluther").order_by('-id')[:4]

    for product in all_data:
        average_rating = Customer_Review.objects.filter(product=product).aggregate(Avg('review_star'))['review_star__avg']
        print('999999999999999999999999999999999999',average_rating)

        if average_rating is not None:
            average_rating = round(average_rating)
        else:
            average_rating = None

        product.average_rating = average_rating

    # user = customer_user.objects.get(email=request.user.email)
    user1 = request.user

    all_blog = BlogPost.objects.all()
    
    for i in all_blog:
        print('fffffffffffffffffff',i.image1,i.image2)

    all_product = product_seller.objects.all()

    for product in all_product:
        average_rating = Customer_Review.objects.filter(product=product).aggregate(Avg('review_star'))['review_star__avg']
        print('999999999999999999999999999999999999',average_rating)

        if average_rating is not None:
            average_rating = round(average_rating)
        else:
            average_rating = None

        product.average_rating = average_rating

    events = Event.objects.all()
    event_discount = Event.objects.filter(event_date=datetime.now().date()).values('event_discount', 'event_name')
    
    for event in event_discount:
       event['event_discount'] *= 100


    data = Wishlist.objects.filter(user = user1)
    count = data.count()
    print('sssssssssssssss',data)
   
    context={
    'all_data':all_data,
    # 'user':user,
    'count':count,
    'all_blog':all_blog,
    'all_product':all_product,
    'data2':data2,
    'data1':data1,
    'data3':data3,
    'data4':data4,
    'data5':data5,
    'data6':data6,
    'data7':data7,
    'data8':data8,
    'data9':data9,
    'data10':data10,
    'data11':data11,
    'user':user,
    'event_discount':event_discount,
   
    }

    return render(request, "customer_base.html", context)


def seller_registeration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        mydata = VrUser(company_name=company_name,company_address=company_address,first_name=first_name, last_name=last_name, email=email,username=email, mobile_number=mobile_number,is_Vruser=True,is_active=True,is_seller=True)
        mydata.set_password(password)
        mydata.save()
        
        seller_profile = seller_user(user=mydata,company_address=company_address,company_name=company_name, first_name=first_name, last_name=last_name, email=email, mobile_number=mobile_number, is_seller=False,is_active=True)
        seller_profile.save()
        
        # subject = "Seller Registration Confirmation"
        # message = f"Hello {mydata.first_name} {mydata.last_name},\n\nThank you for registering as a seller on our website. Your account has been successfully created.\n\n"
        # message += f"Your login details:\n"
        # message += f"Username: {mydata.email}\n"
        # message += f"Password: {password}\n\n"  # Replace [YourGeneratedPassword] with the actual generated password
        # login_url = "http://vishwaratna.in/seller_login/"  # Replace 'seller_login' with the actual name of your seller login URL pattern
        # message += f"To log in, please visit: {login_url}\n\n"
        # message += "Best regards,\nVR Team"
        # from_email = "myvishwaratna@gmail.com"  # Replace this with your desired 'from' email address
        # recipient_list = [mydata.email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return redirect('/seller_login/')
    return render(request,'login/seller_registration.html')



from .models import seller_user

def seller_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        vr_user = authenticate(email=email, password=password)

        if vr_user is not None:
            # Get the associated seller_user instance
            try:
                seller_profile = seller_user.objects.get(user=vr_user)
            except seller_user.DoesNotExist:
                seller_profile = None

            if seller_profile is not None and seller_profile.is_seller:
                # Log in the user
                login(request, vr_user)
                return redirect('/seller_dashboard/')
            else:
                # Handle the case where the seller_user instance doesn't exist
                error_message = "Seller profile not found."
                messages.error(request, error_message)
        else:
            error_message = "Invalid login credentials. Please try again."
            messages.error(request, error_message)

    return render(request, 'login/seller_login.html')

@login_required(login_url='/seller_login/')
def seller_dashboard(request):
   
    user = seller_user.objects.get(email=request.user.email)
    context={
        'user':user,
    }
    return render(request,'seller_base.html',context)


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        VrUser = authenticate(email=email, password=password)
        print("userr",VrUser)

        if VrUser is not None and VrUser.is_superuser:
            # Log in the user
            login(request,VrUser)
            
            return redirect('/admin_dashboard/')  
        else:
           
            error_message = "Invalid login credentials. Please try again."
            messages.error(request, error_message)
            # return render(request, 'registeration/customer_register.html', {'error_message': error_message})

    return render(request, 'login/admin_login.html')

@login_required
def admin_dashboard(request):
    return render(request,'admin_base.html')


def generate_otp():
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp

# Password Reset
from django.shortcuts import get_object_or_404

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if the email exists in the database
        users_with_email = VrUser.objects.filter(email=email)

        if not users_with_email.exists():
            # Handle the case where the email is not found
            return render(request, 'login/password_reset.html', {'error_message': 'Email not found'})

        # Choose one user (you might want to add more logic here based on your requirements)
        user = users_with_email.first()

        # If the email exists, generate and send OTP
        otp = generate_otp()
        subject = 'Password Reset Confirmation'
        message = f'Hello {email},\n\n Your OTP is {otp}\n\nBest regards,\nVR Team'
        from_email = 'vishwaratnasite@gmail.com'  # Replace this with your desired 'from' email address
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Store the email in the session to use it in the password_change view
        request.session['reset_email'] = email

        return render(request, 'login/otp.html', {'otp': otp, 'email': email})

    return render(request, 'login/password_reset.html')


def password_change(request):
    if request.method == 'POST':
        email_from_session = request.session.get('reset_email')
        if not email_from_session:
            # Handle the case where the email is not found in the session
            return render(request, 'login/password_reset.html', {'error_message': 'Invalid request'})

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = email_from_session

        # Check if the passwords match
        if password1 != password2:
            return render(request, 'login/otp.html', {'error_message': 'Passwords do not match'})

        # Get the user with the provided email
        user = VrUser.objects.get(email=email)

        # Set the new password for the user
        user.set_password(password1)
        user.save()

        # Clear the email from the session after password change
        del request.session['reset_email']

        return redirect('/customer_login/')

    return render(request, 'login/otp.html')

@login_required(login_url='/customer_login/')
def customer_profile(request):
    print('111111111111111111111',request.user.email)
    data = customer_user.objects.get(email= request.user.email)
    print('data',data)
    if request.method == 'POST':
        data.first_name =request.POST.get('first_name')
        data.last_name =request.POST.get('last_name')
        data.date_of_birth = request.POST.get('date_of_birth')   
        data.mobile_number = request.POST.get('mobile_number')
        data.locality = request.POST.get('locality')
        data.pincode = request.POST.get('pincode')
        data.city = request.POST.get('city')
        data.state = request.POST.get('state')
        
        data.email = request.POST.get('email')
        image = request.FILES.get('image')
        if image:
            # Delete the previous image if it exists
            if data.image:
                data.image.delete()

            # Save the new profile picture to the user's profile
            data.image = image
        
        data.save()

        return redirect('/customer_after_login/')

        
    user = customer_user.objects.get(email=request.user.email)
    
    context = {
    'data':data,
    'user':user,
    }
        
    return render(request,'login/customer_profile.html',context)




@login_required(login_url='/customer_login/')
def customer_profile_checkout(request):
    print('111111111111111111111',request.user.email)
    data = customer_user.objects.get(email= request.user.email)
    print('data',data)
    if request.method == 'POST':
        data.first_name =request.POST.get('first_name')
        data.last_name =request.POST.get('last_name')
        data.date_of_birth = request.POST.get('date_of_birth')   
        data.mobile_number = request.POST.get('mobile_number')
        data.locality = request.POST.get('locality')
        data.pincode = request.POST.get('pincode')
        data.city = request.POST.get('city')
        data.state = request.POST.get('state')
        
        data.email = request.POST.get('email')
        image = request.FILES.get('image')
        if image:
            # Delete the previous image if it exists
            if data.image:
                data.image.delete()

            # Save the new profile picture to the user's profile
            data.image = image
        
        data.save()

        return redirect('/checkout/')

        
    user = customer_user.objects.get(email=request.user.email)
    
    context = {
    'data':data,
    'user':user,
    }
        
    return render(request,'login/customer_profile_checkout.html',context)



def change_password(request):
   
    print(request.user.email)
    error_message = ''
    message = ''
    print(request.user.email)
    data = VrUser.objects.get(email=request.user.email)
    print('data', data)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_pass1 = request.POST.get('new_pass1')
        new_pass2 = request.POST.get('new_pass2')

        if new_pass1 and new_pass2:
            if new_pass1 != new_pass2:
                error_message = 'Passwords do not match.'
            elif len(new_pass1) < 8:
                error_message = 'Password must be at least 8 characters long.'
            elif len(new_pass1) > 100:
                error_message = 'Password cannot exceed 100 characters.'    
            elif not re.match(r'^(?=.*[a-zA-Z])(?=.*[@!#$])(?=.*[0-9])[a-zA-Z0-9@!#$]{8,}$', new_pass1):
              error_message = 'Password must contain lowercase and uppercase letters (a to z or A to Z), numbers (0 to 9), and at least one of the symbols @, !, #, or $.'
            else:
                user = VrUser.objects.get(username=request.user.username)
                check_password(password, user.password)
                user.password = make_password(new_pass1)
                user.save()
                message = 'Password updated successfully.'
                if request.user.is_customer:
                    return redirect('/customer_login/')
                if request.user.is_admin:
                    return redirect('/admin_login/')
                if request.user.is_seller:
                    return redirect('/seller_login/')
    return render(request, 'login/changepass.html', {'error_message': error_message, 'message': message})

       
@login_required(login_url='/seller_login/')
def seller_profile(request):
    if request.method == 'POST':
        # Existing code to update the seller profile
        data = seller_user.objects.get(email=request.user.email)
        
        # Update the seller profile
        data.first_name = request.POST.get('first_name')
        data.last_name = request.POST.get('last_name')
        data.mobile_number = request.POST.get('mobile_number')
        data.company_name = request.POST.get('company_name')
        data.company_address = request.POST.get('company_address')
        data.pincode = request.POST.get('pincode')
        data.email = request.POST.get('email')
        
        pan_card = request.FILES.get('pan_card')
        aadhar_card = request.FILES.get('aadhar_card')
        gst_document = request.FILES.get('gst_document')
        image = request.FILES.get('image')
        
        if image:
            # Delete the previous image if it exists
            if data.image:
                data.image.delete()
            data.image = image
        
        if pan_card:
            data.pan_card = pan_card
        if aadhar_card:
            data.aadhar_card = aadhar_card
        if gst_document:
            data.gst_document = gst_document
        
        data.save()
        
        # Update or create VrUser instance
        login_user, created = VrUser.objects.get_or_create(email=data.email)
        login_user.first_name = data.first_name
        login_user.last_name = data.last_name
        login_user.save()
        
        if data.seller_reject:
            data.seller_reject = False
            data.seller_approved = False
        else:
            data.seller_approved = False
        data.save()

        return redirect('/seller_dashboard/')

    else:
        # Handle GET request to display seller profile page
        data = seller_user.objects.get(email=request.user.email)
        user = seller_user.objects.get(email=request.user.email)
        
        context = {
            'data': data,
            'user': user,
        }
        
        return render(request, 'login/seller_profile.html', context)


def customer_logout(request):
    logout(request)
    return redirect('/')

def seller_logout(request):
    logout(request)
    return redirect('/seller_login/')

def admin_logout(request):
    logout(request)
    return redirect('/admin_login/')


def contact_us(request):
    if request.method == 'POST':
        # Retrieve form data directly from request.POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')

        # Create a Contact object and save it to the database
        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            comment=comment
        )

        home_url = reverse('home')
        return redirect(home_url)

        return redirect('//')  # Redirect to a success page or another page

    return render(request,'footer/contact_us.html')



def privacy_policy(request):
    return render(request,'footer/privacy_policy.html')


def refund_and_return(request):
    return render(request,'footer/refund_and_return.html')

def terms_and_condition(request):
    return render(request,'footer/terms_and_condition.html')

def shopping_faqs(request):
    return render(request,'footer/shopping_faqs.html')


def blog_bhagatsingh(request,title):
    blog = BlogPost.objects.get(title=title)
    print('fdddddddddd',blog)
    context={
        'blog':blog,
    }
    return render(request,'blogs/view_blog_title.html',context)


def cust_blog_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        VrUser = authenticate(email=email, password=password)
        print("userr",VrUser)

        if VrUser is not None and VrUser.is_customer:
            # Log in the user
            login(request,VrUser)
            
            blog = BlogPost.objects.all()
            print('aaaaaaaaaaaaaaaaa',blog)
            
            return redirect('/blog_bhagatsingh/Bhagat Singh/')  
        else:
           
            error_message = "Invalid login credentials. Please try again."
            messages.error(request, error_message)
            # return render(request, 'registeration/customer_register.html', {'error_message': error_message})

    return render(request, 'login/customer_login.html')



@login_required(login_url='/admin_login/')
def admin_profile(request):
    print('admin',request.user.email)
    data1 = VrUser.objects.get(email= request.user.email)
  
    print('data1',data1)
    if request.method == 'POST':
        data1.first_name =request.POST.get('first_name')
        data1.last_name =request.POST.get('last_name')
        image = request.FILES.get('image')
        if image:
            # Delete the previous image if it exists
            if data1.image:
                data1.image.delete()

            # Save the new profile picture to the user's profile
            data1.image = image
        
        data1.save()

        return redirect('/admin_dashboard/')

        
    user = VrUser.objects.get(email=request.user.email)
    
    context = {
    'data1':data1,
    'user':user,
    'first_name': data1.first_name,
    'last_name': data1.last_name,
    'image':data1.image
    }
        
    return render(request,'login/admin_profile.html',context)

# def pages(request):
#     context = {}
#     try:
#         html_template = loader.get_template( 'page-404.html' )
#         return HttpResponse(html_template.render(context, request))
#     except:
    
#         html_template = loader.get_template( 'page-500.html' )
#         return HttpResponse(html_template.render(context, request))



from .models import StoreSettings

def store_settings(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        store_email = request.POST.get('store_email')
        store_description = request.POST.get('store_description')
        store_logo = request.FILES.get('store_logo')
        store_contact_number = request.POST.get('store_contact_number')
        store_address = request.POST.get('store_address')
        store_city = request.POST.get('store_address')
        store_state = request.POST.get('store_address')
        store_pincode = request.POST.get('store_address')
        pan_no = request.POST.get('store_address')
        gst_no = request.POST.get('store_address')

        # Update or create store settings object
        settings= StoreSettings.objects.update_or_create(
            defaults={
                'store_name': store_name,
                'store_logo': store_logo,
                'store_email': store_email,
                'store_contact_number': store_contact_number,
                'store_address': store_address,
                'store_description':store_description,
                'store_city':store_city,
                'store_state':store_state,
                'store_pincode':store_pincode,
                'pan_no':pan_no,
                'gst_no':gst_no
            }
        )
        return redirect('/admin_dashboard/')  

    # Retrieve existing store settings if available
    settings = StoreSettings.objects.first()
    

    return render(request, 'login/store_settings.html', {'settings': settings})



def customer_before_login(request,prod_id):
    print("prod_id",prod_id)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('jjjjjjjjjjjjjjjj',prod_id)
        # Authenticate user
        VrUser = authenticate(email=email, password=password)
        print("userr",VrUser)

        if VrUser is not None and VrUser.is_customer:
            data = prod_id
            print('data',data,prod_id)
            # Log in the user
            login(request,VrUser)
            
            url=reverse('prod_details',args=[data])
            print('ssssssssss',url,data)
            return redirect(url)
            
              
        else:
           
            error_message = "Invalid login credentials. Please try again."
            messages.error(request, error_message)
            # return render(request, 'registeration/customer_register.html', {'error_message': error_message})
    context={
        'prod_id':prod_id,
    }
    return render(request, 'login/customer_before_login.html',context)