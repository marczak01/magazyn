from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path("dashboard/", views.dashboard, name='dashboard'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("register/", views.register, name='register'),
    path("warehouses/", views.warehouse, name='warehouse'),
    path("warehouses/<slug:slug>/", views.warehouse_stock, name="warehouse_stock"),
]
