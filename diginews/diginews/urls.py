from django.contrib import admin
from django.urls import path , include #i add include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog'))
]
