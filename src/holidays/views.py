from django.shortcuts import render

# Create your views here.
def holidays_list(request):
    return render(request, 'holidays/holidays_list.html')