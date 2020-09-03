from django.urls import path
from twitteruser import views as v


urlpatterns = [
    path('', v.index, name='homepage'),
    path('edit/', v.edit_profile, name='editprofile'),
]
