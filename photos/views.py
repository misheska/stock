from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.conf import settings

import securepay.gateway
from photos.models import Photo, PurchaseLog

from photos.models import CouponCode

def index(request):
    photos = Photo.objects.all()

    context = {
        'photos': photos,
    }
    return render(request, 'index.html', context)

def details(request, photo_id):
    photo = get_object_or_404(Photo, id=int(photo_id))

    context = {
        'photo': photo,
    }
    return render(request, 'details.html', context)

def checkout(request):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))

    photo_price = settings.PHOTO_PRICE

    coupon_code = None
    if request.method == "POST":
        code = request.POST.get('code', '')
        photo_price, coupon_code = get_discount_info(code, photo_price)

    context = {
        'photo': photo,
        'photo_price': photo_price,
        'coupon_code': coupon_code,
    }
    return render(request, 'checkout.html', context)

def buy(request):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))

    cc = request.POST.get('cc')
    exp = request.POST.get('exp')
    name = request.POST.get('name')
    code = request.POST.get('code')
    price, coupon_code = get_discount_info(code, settings.PHOTO_PRICE)

    securepay.gateway.purchase(price, cc, exp, name)
    record_purchase(photo, price)

    context = {
        'photo': photo,
        'amount': price,
    }
    return render(request, 'buy.html', context)

def get_discount_info(code, price):
    try:
        coupon_code = CouponCode.objects.get(code=code)
    except CouponCode.DoesNotExist:
        return price, None
    else:
        return coupon_code.apply_discount(price), coupon_code

def record_purchase(photo, amount):
    PurchaseLog.objects.create(
        photo=photo,
        amount=amount,
    )

def purchase_log(request):
    logs = PurchaseLog.objects.all()

    context = {
        'logs': logs,
    }
    return render(request, 'purchase_log.html', context)

def create_coupon(request):
    if request.method == "POST":
        percentage = int(request.POST.get('discount_percentage', 0))
        code = request.POST.get('code')

        coupon_code = CouponCode.objects.create(
            discount_percentage=percentage,
            code=code,
        )

        context = {
            'coupon_code': coupon_code
        }
        return render(request, 'admin_coupon_created.html', context)

    return render(request, 'admin_create_coupon.html', {})
