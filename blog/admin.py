from django.contrib import admin
from .models import Post, Category, Tag, Comment

# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin): #URL로 사용하기 적합하지 않은 문자를 적절하게 변환한 다음 slug에 채워줌
    prepopulated_fields = {'slug' : ('name',)} # Category 모델의 name필드에 값이 입력됐을 때 자동으로 slug가 만들어진다.

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)