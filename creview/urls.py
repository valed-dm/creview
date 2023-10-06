"""
URL configuration for a creview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from files.views import FilesTableView
from files.views import csv_table
from files.views import customize_csv
from files.views import customized
from files.views import upload_file
from users.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("files_table/", FilesTableView.as_view(), name="files_table"),
    path("upload/", upload_file, name="upload"),
    path("csv_table/", csv_table, name="csv_table"),
    path("customize_csv/", customize_csv, name="customize_csv"),
    path("customized/", customized, name="customized"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
