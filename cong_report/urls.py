"""cong_report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from frontend.views import PublisherAutocomplete, get_report

from frontend.views import cong_submission


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", cong_submission),
    path("<str:congregation_code>/", cong_submission),
    path("report/<int:group_id>/", get_report),
    path("report/<int:group_id>/<int:year>/<int:month>", get_report),
    path(
        r"^publisher-autocomplete/$",
        PublisherAutocomplete.as_view(),
        name="publisher-autocomplete",
    ),
]

admin.site.site_header = "Field Service Group Admin"
