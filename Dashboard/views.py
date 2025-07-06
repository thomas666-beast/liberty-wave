from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Dashboard Views

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
