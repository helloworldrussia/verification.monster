from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login_page"),
    path('login', views.LoginView.as_view(), name="mirror_login_page"),

    path('user/', include("users.urls")),
    path('accounts/', include("accounts.urls")),
    
    path('form/user/', include("users.form_urls")),

    path('admin/', admin.site.urls),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
