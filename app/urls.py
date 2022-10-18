# from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.conf import settings
from django.conf .urls .static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm ,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    # path('', views.home),
    path('' ,views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.productDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    # login authentication
    path('accounts/profile/',views.ProductView.as_view(),name="home"),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name ='app/passwordchange.html' ,form_class=MyPasswordChangeForm ,success_url='/passwordchangedone/'), name='passwordchange'),

    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name="app/passwordchangedone.html"),name='passwordchangedone'),


    path ('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path ('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_resetdone.html'),name='password_resetdone'),

    path ('password-resetcomplete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_resetconfirm.html'),name='password_resetcomplete'),

    path('password-resetconfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_resetconfirm.html', form_class= MySetPasswordForm) ,name='password_resetconfirm'),
    #  end of login

    path ('registration/',views.CustomerRegistrationView.as_view(), name="customerregistration"),
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
