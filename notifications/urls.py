from django.urls import path
from notifications import views as v

urlpatterns = [
    path('notifications/', v.NotificationView.as_view(), name="notifications"),
]
