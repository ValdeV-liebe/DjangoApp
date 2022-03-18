from django.urls import path 
from store.views import *

urlpatterns = [
    path('listing' , listing , name = "listing"),
    path('detail/<int:album_id>' , detail , name = "detail"),
    path('search/' , search , name = "search"),
    path('liste/' , liste , name = "liste"),
    path('artist/' , artist , name = "artist"),
]
