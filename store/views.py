# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product, CartItem, WishlistItem, Order
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Initialize Razorpay Client
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

# User Signup


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. Please login.")
            return redirect('signin')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

# User Signin


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'store/signin.html')

# User Logout


def signout(request):
    logout(request)
    return redirect('signin')

# Product List with Search and Category Filter


def product_list(request):
    query = request.GET.get('query', '')
    category_slug = request.GET.get('category')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query))

    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query
    })

# Product Detail


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


# Add to Cart
@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# View Cart


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price *
                      item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Update Cart Item Quantity


@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        total_price = sum(
            item.product.price * item.quantity for item in CartItem.objects.filter(user=request.user))
        return JsonResponse({'status': 'success', 'totalPrice': total_price})

# Remove Item from Cart


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    total_price = sum(item.product.price *
                      item.quantity for item in CartItem.objects.filter(user=request.user))
    return JsonResponse({'status': 'success', 'totalPrice': total_price})

# Add to Wishlist


@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

# View Wishlist


@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

# Remove from Wishlist


@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(
        WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

# Move Item from Wishlist to Cart


@login_required
def move_to_cart(request, item_id):
    wishlist_item = get_object_or_404(
        WishlistItem, id=item_id, user=request.user)
    add_to_cart(request, wishlist_item.product.slug)
    wishlist_item.delete()
    return redirect('cart')


# # Checkout and Create Razorpay Order
# @login_required
# def checkout(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     total_amount = sum(item.product.price *
#                        item.quantity for item in cart_items)

#     # Create Razorpay Order
#     razorpay_order = razorpay_client.order.create({
#         "amount": int(total_amount * 100),  # Amount in paise
#         "currency": "INR",
#         "payment_capture": "1"  # Automatic capture after payment
#     })

#     # Save Order in Database
#     order = Order.objects.create(
#         user=request.user,
#         total_amount=total_amount,
#         razorpay_order_id=razorpay_order['id']
#     )
#     order.product.set([item.product for item in cart_items])

#     return render(request, 'store/checkout.html', {
#         'order': order,
#         'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#         'amount': total_amount * 100,  # Amount in paise
#         'currency': 'INR',
#         'razorpay_order_id': razorpay_order['id']
#     })

# # Handle Payment Success


# @csrf_exempt
# def payment_success(request):
#     if request.method == 'POST':
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         razorpay_signature = request.POST.get('razorpay_signature')

#         # Verify Payment Signature
#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         }

#         try:
#             razorpay_client.utility.verify_payment_signature(params_dict)
#             order = Order.objects.get(razorpay_order_id=razorpay_order_id)
#             order.razorpay_payment_id = razorpay_payment_id
#             order.razorpay_signature = razorpay_signature
#             order.status = 'Paid'
#             order.save()

#             # Clear user's cart after successful payment
#             CartItem.objects.filter(user=request.user).delete()

#             return render(request, 'store/payment_success.html', {'order': order})

#         except razorpay.errors.SignatureVerificationError:
#             return render(request, 'store/payment_failed.html')

#     return redirect('product_list')
