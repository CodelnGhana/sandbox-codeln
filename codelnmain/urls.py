"""codelnmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

from accounts.views import profile

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/<int:pk>', profile, name='view_profile'),
    path('projects/', include('projects.urls', namespace='projects')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include('frontend.urls', namespace='frontend')),
    path('', include('classroom.urls')),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('testing/', include('testing.urls', namespace='testing')),
    path('marketplace/', include('marketplace.urls', namespace='marketplace')),
    path('blog/', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'frontend.views.page_404'
handler500 = 'frontend.views.page_500'
