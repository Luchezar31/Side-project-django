
from django.urls import path, include

from posts import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home-page'),
    path('dashboard/',views.Dashboard.as_view(),name="dashboard"),
    path('post/',include([
        path('add/',views.CreatePost.as_view(),name='add-post'),
        path('delete/<int:pk>/',views.DeletePost.as_view(),name='delete-post'),
        path('details/<int:pk>',views.DetailPost.as_view(),name='post-details'),
        path('edit/<int:pk>/',views.EditPost.as_view(),name='edit-post'),
    ]))
]



