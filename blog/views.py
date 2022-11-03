from django.shortcuts import render
from . models import Post, Category
from django.views.generic import ListView, DetailView

# Create your views here.
class PostList(ListView): #CBV방식
    model = Post
    ordering = '-pk' #pk값이 작은 순서대로

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all() #모든 카테고리를 가져옴
        context['no_category_post_count'] = Post.objects.filter(category=None).count #카테고리가 지정되지 않은 포스트의 개수를 세라
        return context
    # 템플릿은 모델명_list.html : post_list.html
    # 매개변수 모델명_list : post_list

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    # 템플릿은 모델명_detail.html : post_detail.html
    # 매개변수 모델명 : post

def category_page(request, slug):
    if slug == 'no_category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html', {
        'category' : category,
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })

#def index(request): #FBV방식
#   posts = Post.objects.all().order_by('-pk') pk값의 역순으로 정렬
#  return render(request, 'blog/index.html', {'posts': posts})
#
#def single_post_page(request, pk):
#   post1 = Post.objects.get(pk=pk) 괄호 안의 조건을 만족하는 Post 레코드를 가져오라
#  return render(request, 'blog/single_post_page.html', {'post': post1})
