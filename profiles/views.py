from django.shortcuts import render

# Create your views here.
def profile(request):
    """ A view to return the profile.html page """
    return render(request, 'profiles/profile.html')