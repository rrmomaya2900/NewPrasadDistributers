"""
URL configuration for GST_Declaration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from GST_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('gst-form/', views.gst_form_view, name='gst_form'),
    path('api/submit-gst/', views.submit_gst_form, name='submit_gst_form'),
    path('success/', views.success_page, name='success_page'),
    path('api-auth/', include('rest_framework.urls')),
    path('form/', views.gst_form_view, name='form'),
    path('upload_documents/', views.upload_documents, name='upload_documents'),
    path('verify-gst/', views.verify_gst, name='verify_gst'),
    path('document_form/', views.document_form, name='document_form'),
    path('success_end/', views.success_end, name='success_end'),
    path("success_end/<str:gst_number>/", views.generate_updated_pdf, name='generate_updated_pdf'),
    path("acknowledgement/<str:gst_number>/", views.generate_acknowledgement_pdf, name="generate_acknowledgement_pdf"),
    path('home/', views.back_to_home, name='back_to_home'),
]

# Only if using MEDIA files (e.g., during local dev)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)