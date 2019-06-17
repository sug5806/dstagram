from django.urls import path

from .views import *

app_name = 'photo'

urlpatterns = [
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('favorite/<int:photo_id>/', PhotoSave.as_view(), name='favorite'),
    path('create/', PhotoCreate.as_view(), name='create'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name='delete'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name='detail'),
    path('like/', PhotoLikeList.as_view(), name='like_list'),
    path('favorite/', PhotofavoriteList.as_view(), name='favorite_list'),
    path('', PhotoList.as_view(), name='index'),
    path('pa/', PhotoView.as_view())
]
