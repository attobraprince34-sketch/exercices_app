from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Administration Praxis"
admin.site.site_title = "Praxis — Administration"
admin.site.index_title = "Gestion du contenu pédagogique"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cursus.urls")),
]
