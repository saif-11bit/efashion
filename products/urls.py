from django.urls import path
from .views import (
    landing,
    category_item,
)



urlpatterns = [
    path('', landing, name="landing"),
    path('<int:id>/', category_item, name="landing"),
]
