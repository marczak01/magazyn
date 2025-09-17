from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
import random

#@login_required
def warehouse(request):
    return render(request, "account/warehouse.html")

def warehouse_stock(request, slug):
    """
    DEMO: generujemy 30 pozycji, żeby łatwo przetestować scroll w kafelku.
    Gdy podepniesz modele, wypełnij `stock_rows` danymi z bazy (te same klucze).
    """
    locations = ["WH/029114", "WH/029122", "WH/029905"]
    stock_rows = []
    for i in range(1, 31):
        idx3 = f"{i:03d}"
        stock_rows.append({
            "name":     f"Gino Vega ALT{idx3}-C3",
            "sku":      f"ALT{idx3}-C3",
            "lot":      f"SN-{i:04d}",
            "location": random.choice(locations),
            "reserved": random.choice([0, 0, 1, 2]),           # trochę zer dla realizmu
            "qty":      random.choice([0, 1, 2, 3, 5, 7, 8, 10, 12]),
            "orders":   random.choice([0, 0, 0, 1, 2, 3, 5]),
            "value":    random.choice([119, 149, 159, 179, 199, 219, 259, 269, 289, 309, 339]),
        })

    context = {
        "warehouse_name": (slug or "MAG 1").upper(),
        "stock_rows": stock_rows,
    }
    return render(request, "account/warehouse_stock.html", context)
    
#@login_required
def dashboard(request):
    # Placeholdery do UI – podłączysz do modeli, gdy będą gotowe
    context = {
        "kpi": {
            "products": 1280,
            "orders_in_progress": 14,
            "orders_progress": 42,   # % do paska postępu
            "low_stock": 6,
            "returns": 2,
        },
        "low_stock": [
            {"name": "Pudełko kartonowe 30x20x10", "sku": "BOX-302010", "qty": 4, "min_qty": 10},
            {"name": "Taśma pakowa 48mm",          "sku": "TAPE-48",   "qty": 12, "min_qty": 20},
            {"name": "Folia stretch 2kg",          "sku": "STRETCH-2", "qty": 1, "min_qty": 5},
        ],
        "recent": [
            {"title": "Dodano produkt", "subtitle": "Organizer biurkowy metalowy", "when": "2 h temu"},
            {"title": "Zmieniono cenę", "subtitle": "Mata antystatyczna ESD",       "when": "wczoraj"},
            {"title": "Nowe zamówienie", "subtitle": "Zam. #ZAM-2025/0818/004",     "when": "wczoraj"},
        ],
    }
    return render(request, "account/dashboard.html", context)


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

def register(request):
    return render(request, "account/register.html")