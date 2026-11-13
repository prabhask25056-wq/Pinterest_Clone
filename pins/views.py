
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, PinForm
from .models import Pin
from .supabase_client import upload_image



def register_view(request):

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")

    return render(request, "pins/register.html", {"form": form})



@login_required
def main_view(request):

    pins = Pin.objects.all()

    return render(request, "pins/main.html", {"pins": pins})



@login_required
def add_view(request):

    form = PinForm()

    if request.method == "POST":
        form = PinForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data["image"]
            url = upload_image(image)

            Pin.objects.create(
                user=request.user,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                image_url=url
            )

            return redirect("main")

    return render(request, "pins/add.html", {"form": form})
