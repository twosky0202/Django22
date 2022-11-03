from django.urls import path
from . import views

urlpatterns = [ # IP주소/blog/
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()), #CBV방식
    path('category/<str:slug>/', views.category_page)
    #path('', views.index), # IP주소/blog/
    #path('<int:pk>/', views.single_post_page) #FBV(Function Based View)방식
]