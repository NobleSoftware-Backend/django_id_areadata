# Django_id_areadata

## Required dependencies

To use this app, you need to have these requirements:
- django >= 5.0
- djangorestframework (for the area endpoints)
- drf-spectacular (for swagger schema)
- django-filter (for the area endpoints)

## How to use

In your settings file, add this app name to your INSTALLED_APPS list below the requirements above, like this:
```
INSTALLED_APPS = [
  ...
  "rest_framework",
  "drf_spectacular",
  "django_filters",
  "django_id_areadata"
]
```

Then after that in your project urls, include the urlpatterns from this app, as follows:
```
from django.urls import include, path

urlpatterns = [
  ...
  path("area/", include("django_id_areadata.urls"))
]
```


And then you can run `python manage.py updatearea` to populate the area data for the first time.


## License
- This package and repository are licensed under the MIT License.
- All data that included in this package and repository are made available under the Open Database License.
These licenses apply to the current and previous versions, and apply to future versions until changed.
