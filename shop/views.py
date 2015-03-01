from django.shortcuts import render


def index(request):
    """
    View for landing/home page
    """
    return render(request, 'index.html')
