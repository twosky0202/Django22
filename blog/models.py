from django.db import models
from django.contrib.auth.models import User
import os.path

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) #각 카테고리의 이름을 담는 필드. unique=True: name 중복 불가
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # SlugField는 사람이 읽을 수 있는 텍스트로 고유 URL을 만들고 싶을때

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/' #고유 URL

    class Meta:
        verbose_name_plural = 'Categories' #복수형 직접 지정

class Post(models.Model):
    title = models.CharField(max_length=30) #문자를 담는 피드. 최대 길이 30, 제목
    hook_text = models.CharField(max_length=100, blank=True) #요약문
    content = models.TextField() #문자열의 길이 제한이 없음, 내용

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True) #포스트 이미지 올리기
    # upload_to='이미지를 저장할 폴더의 경로규칙' =>blog폴더 아래 images폴더 만들고 연도폴더, 월폴더, 일폴더 밑 위치,
    # blank=Ture: 해당필드는 필수항목은 아니다. %Y 2022, %y 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True) #포스트에 파일 올리기

    created_at = models.DateTimeField(auto_now_add=True) #월, 일, 시, 분, 초 기록(시간 자동으로 저장), 작성일
    update_at = models.DateTimeField(auto_now=True) #(수정시간 자동으로 저장), 수정일

    # 작성자 정보. on_delete=models.CASCADE: 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 이 포스트도 같이 삭제한다.
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  #이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 작성자명을 빈칸으로둔다.

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) #blank=True: 관리자페이지에서 카테고리 빈칸 가능

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}' #관리자페이지에서 pk값, 제목, 작성자, 날짜 보이기

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self): #파일경로제외 파일명만나오게
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self): #확장자찾기
        return self.get_file_name().split('.')[-1] # a.b.txt => a b txt

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
           return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
           return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'