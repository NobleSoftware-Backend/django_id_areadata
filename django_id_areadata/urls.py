from django.urls import path

from django_id_areadata import views

urlpatterns = [
    path("provinces/", views.ProvinceList.as_view(), name="provinces-list"),
    path("regencies/", views.RegencyList.as_view(), name="regencies-list"),
    path("districts/", views.DistrictList.as_view(), name="districts-list"),
    path("subdistricts/", views.SubDistrictList.as_view(), name="subdistricts-list"),
]
