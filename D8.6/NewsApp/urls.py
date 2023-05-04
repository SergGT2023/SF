from django.urls import path
from .views import (
    PostsList, PostDetail, PostCreateNW, PostEditNW, PostDeleteNW, PostsSearch, PostCreateAR, PostDeleteAR, PostEditAR,)

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreateNW.as_view(), name='post_createNW'),
    path('<int:pk>/edit/', PostEditNW.as_view(), name='post_editNW'),
    path('<int:pk>/delete/', PostDeleteNW.as_view(), name='post_deleteNW'),
    path('search/', PostsSearch.as_view(), name='post_search'),
    path('create2/', PostCreateAR.as_view(), name='post_createAR'),
    path('<int:pk>/delete2/', PostDeleteAR.as_view(), name='post_deleteAR'),
    path('<int:pk>/edit2/', PostEditAR.as_view(), name='post_editAR'),
    path('sign/', PostsList.as_view(),name='sign.urls')
]