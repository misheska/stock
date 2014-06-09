from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.conf import settings

import securepay.gateway
from photos.models import Photo, PurchaseLog


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

    context = {
        'photo': photo,
        'photo_price': settings.PHOTO_PRICE,
    }
    return render(request, 'checkout.html', context)

def buy(request):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))

    cc = request.POST.get('cc')
    exp = request.POST.get('exp')
    name = request.POST.get('name')
    price = settings.PHOTO_PRICE

    securepay.gateway.purchase(price, cc, exp, name)
    record_purchase(photo, price)

    context = {
        'photo': photo,
        'amount': price,
    }
    return render(request, 'buy.html', context)

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
