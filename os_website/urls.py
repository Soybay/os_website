from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data_collection.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line
]
