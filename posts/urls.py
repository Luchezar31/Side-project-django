from django.urls import path, include

from posts import views

urlpatterns = [
    path('',views.home_page,name='home-page'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('post/',include([
        path('add/',views.add_post,name='add-post')
    ]))
]
