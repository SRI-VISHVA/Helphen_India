from .forms import KinderForm
from django.shortcuts import render, redirect


# Create your views here.
def kinder_contact_form(request):
    if request.method == 'POST':
        form = KinderForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    elif request.method == 'GET':
        form = KinderForm()
        return render(request, template_name='PK.html', context={'form': form})
