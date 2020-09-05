from django.urls import path
from notifications import views as v

urlpatterns = [
    path('notifications/', v.notification_view, name="notifications"),
]
