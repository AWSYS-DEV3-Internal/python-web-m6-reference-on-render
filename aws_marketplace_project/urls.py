"""aws_marketplace_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('aws_marketplace_app.urls')),
    path('admin/', admin.site.urls),

    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='security/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="security/password_reset_confirm.html"), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='security/password_reset_complete.html'), 
        name='password_reset_complete'
    )
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static("/uploads/media/user_display_image", document_root=os.path.join(settings.BASE_DIR, 'uploads/media/user_display_image'))
urlpatterns += static("/uploads/media/posting_image", document_root=os.path.join(settings.BASE_DIR, 'uploads/media/posting_image'))