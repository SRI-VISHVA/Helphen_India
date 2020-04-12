from django.shortcuts import render, redirect
from Kinder.models import Contact

# Event's View
def events(request):
    return render(request, template_name='Events.html')


# RxD's View
def rxd(request):
    return render(request, template_name='RxD.html')


# Project Prayas's View
def pp(request):
    return render(request, template_name='PP.html')


# Work's View
def work(request):
    return render(request, template_name='works.html')

# Team's View
def team(request):
    return render(request, template_name='Team.html')


def home_contact_form(request):
    if request.method == 'POST':
        name = request.POST['contactName']
        email_id = request.POST['contactEmail']
        r = request.POST['contactMessage']
        x = Contact(name=name, email_id=email_id, message=message)
        x.save()
        return redirect('home')

    elif request.method == 'GET':
        return render(request, template_name='index1.html')
