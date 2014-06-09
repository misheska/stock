from django.shortcuts import render, redirect

from feature import Feature

def set_enabled(request):
    f = Feature(request.POST['name'])
    enabled = request.POST['enabled'] == 'True'

    if enabled:
        f.enable(request)
    else:
        f.disable(request)

    return redirect("/feature/")

def index(request):
    features = [Feature(name) for name in sorted(Feature.features)]
    features_enabled = [(f, f.is_enabled(request)) for f in features]

    context = {
        'features_enabled': features_enabled,
    }
    return render(request, 'feature/index.html', context)