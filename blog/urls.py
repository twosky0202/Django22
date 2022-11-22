from django.urls import path
from . import views

urlpatterns = [ # IP주소/blog/
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()), #CBV방식
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), #comment의 pk
    path('update_post/<int:pk>/', views.PostUpdate.as_view()), #post의 pk
    path('category/<str:slug>/', views.category_page), #IP주소/blog/category/slug/
    path('tag/<str:slug>/', views.tag_page),#IP주소/blog/tag/slug/
    path('create_post/', views.PostCreate.as_view()),


    #path('', views.index), # IP주소/blog/
    #path('<int:pk>/', views.single_post_page) #FBV(Function Based View)방식
]