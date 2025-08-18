from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')

def login_view(request):
    # Formularz jest w home.html (modal) – tu tylko obsługujemy POST.
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next") or reverse("account:dashboard")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)

        messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło.")
        return redirect("mainapp:home")

    # GET -> wróć na stronę główną i pokaż modal
    messages.info(request, "Zaloguj się, aby kontynuować.")
    return redirect("mainapp:home")

def logout_view(request):
    logout(request)
    messages.success(request, "Wylogowano pomyślnie.")
    return redirect("mainapp:home")
