from django.urls import path
from chain import views

urlpatterns = [
    
    path("", views.userHome, name='userhome'),
    # path("admin-login", views.admin, name='AdminHome'),
    # path("result", views.result, name='resulthome'),
    path("home", views.index, name='home'),
    path("search/<prodid>/", views.userSearch, name='usersearch'),
    # path('signup', views.handleSignUp, name="handleSignUp"),
    # path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('userPanel', views.userPanel, name="userpanel"),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    # path('adminpage/', views.admin, name='adminpage'),
    path('distributor', views.Distributor, name="distributor"),
    path('retailor', views.Retailor, name="retailor"),
    # path('verified', views.Verified, name="verified"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("recomendation/", views.recomendation, name="recomendation"),
    
]
