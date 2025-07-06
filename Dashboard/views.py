from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Dashboard Views

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

