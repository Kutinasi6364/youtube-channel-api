from django.urls import path, include
from . import views

app_name = "channels"
urlpatterns = [
    path("", views.channel_home_view, name="channel_home"),
    path("channellist/", views.channel_list_view, name="channel_list"),
    path("search/", views.channel_search_view, name="channel_search"),
    path("register/", views.register_channel_subscription, name="channel_register"),
    path("unregister/", views.unregister_channel_subscription, name="channel_unregister"),
    path("api/channel_list/", views.channel_view_set, name="channel_api"),
]