from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from cart.models import Cart,Items
from .models import Checkout,Payment,PaymentDone,ProductDetail
import stripe
import json
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    # Fetch the user's latest checkout details, if any
    existing_checkout = Checkout.objects.filter(user=request.user).order_by('-id').first()

    if request.method == 'POST':
        # Save new checkout details from the form submission
        firstname = request.POST['fname']
        lastname = request.POST['name']
        country = request.POST['country']
        address = request.POST['address']
        town_city = request.POST['city']
        postcode_zip = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        cart = Cart.objects.filter(user=request.user).first()

        check = Checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            town_city=town_city,
            postcode_zip=postcode_zip,
            phone=phone,
            email=email
        )
        check.save()
        return redirect('payments')

    # Render the checkout form with existing data pre-filled
    return render(request, 'checkout.html', {'checkout': existing_checkout})


@login_required
def payments(request):
    # Get existing payment details for the logged-in user
    existing_payment = Payment.objects.filter(user=request.user).first()

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        ifc_code = request.POST.get('ifc_code')
        name = request.POST.get('name')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')

        # Validate and save payment details
        if all([account_number, ifc_code, name, expiry_month, expiry_year, cvv]):
            if existing_payment:
                # Update existing payment record
                existing_payment.account_number = account_number
                existing_payment.ifc_code = ifc_code
                existing_payment.name = name
                existing_payment.expiry_month = expiry_month
                existing_payment.expiry_year = expiry_year
                existing_payment.cvv = cvv
                existing_payment.save()
                messages.success(request, "Payment details updated successfully.")
            else:
                # Create new payment record
                Payment.objects.create(
                    user=request.user,
                    account_number=account_number,
                    ifc_code=ifc_code,
                    name=name,
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    cvv=cvv
                )
                messages.success(request, "Payment details saved successfully.")
            return redirect('initiate_payment')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'payment_details.html', {'payment': existing_payment})



def initiate_payment(request):
    total=0
    user = request.user

    if user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)

    # check the section have any products
    else:
        return HttpResponseForbidden('Access Denied')

    # Get latest checkout and payment details
    checkout = Checkout.objects.filter(user=user).last()  # Get the latest checkout object
    payment = Payment.objects.filter(user=user).last()    # Get the latest payment object


    item_items = Items.objects.filter(cart__in=cart_items, active=True)
    for i in item_items:
        total += (i.product.price * i.quantity)


    # Razorpay Client Initialization
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount_in_paisa = total * 100  # Convert rupees to paisa

    # Payment Details
    amount = amount_in_paisa
    currency = 'INR'
    receipt = 'receipt#1'
    notes = {'key': 'value'}  # Optional notes
    # Save payment details




    # Create Order
    razorpay_order = client.order.create({
        'amount': amount,
        'currency': currency,
        'receipt': receipt,
        'notes': notes
    })


    # Save Razorpay order ID temporarily (in session or a model)
    request.session['razorpay_order_id'] = razorpay_order['id']



    # Pass Order Details to Template
    context = {
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount': amount,  # Make sure 'amount' is correctly passed here
        'currency': currency,
        'payment':payment,
        'checkout':checkout,
    }
    return render(request, 'payment.html', context)


from django.http import JsonResponse, HttpResponseForbidden, HttpResponse


from django.shortcuts import get_object_or_404

def payment_success(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden('Access Denied')

    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return HttpResponse('No items in cart.', status=400)

    # Retrieve Razorpay order ID from session
    razorpay_order_id = request.session.get('razorpay_order_id')
    if not razorpay_order_id:
        return HttpResponse('Order ID not found.', status=400)

    # Calculate total amount
    cart_items = Items.objects.filter(cart=cart, active=True)
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create payment record
    payment_done = PaymentDone.objects.create(
        user=user,
        order_id=razorpay_order_id,
        amount=total,  # Amount in rupees
    )

    # Save product details
    for item in cart_items:
        ProductDetail.objects.create(
            payment=payment_done,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            total_price=item.product.price * item.quantity,
        )

        # Reduce product stock
        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart
    cart_items.delete()
    cart.delete()

    return redirect('payment_success_print')



# def stripe_payment(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             payment_method_id = data.get('payment_method_id')
#
#             if not payment_method_id:
#                 return JsonResponse({'success': False, 'error': 'Payment method ID not provided'})
#
#             return_url = request.build_absolute_uri('/stripe_payment_success')
#
#             # Create the PaymentIntent
#             intent = stripe.PaymentIntent.create(
#                 amount=5000,  # Amount in cents ($50.00)
#                 currency="usd",
#                 payment_method=payment_method_id,
#                 confirm=True,
#                 return_url=return_url,
#             )
#
#             # Payment successful
#             if intent['status'] == 'succeeded':
#                 return JsonResponse({'success': True, 'redirect_url': '/home/'})
#             else:
#                 return JsonResponse({'success': False, 'error': 'Payment confirmation incomplete.'})
#
#         except stripe.error.CardError as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return render(
#         request,
#         "stripe_payment.html",
#         {"stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY}
#     )


def payment_success_print(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden('Access Denied')

    payment_done = PaymentDone.objects.filter(user=user).last()
    if not payment_done:
        return HttpResponse('No payment record found.', status=404)

    product_details = ProductDetail.objects.filter(payment=payment_done)

    payment_data = {
        'transaction_id': payment_done.order_id,
        'amount_paid': f"₹{payment_done.amount:.2f}",
        'payment_date': payment_done.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'products': product_details,
    }

    return render(request, 'payment_success.html', payment_data)


