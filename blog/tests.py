from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

# Create your tests here.
class TestView(TestCase):

    def setUp(self): # TestCase에서 기본적으로 설정되어야하는 내용
        self.client = Client() #setUP() 함수 내에 Client()를 사용하겠다. 테스트를 위한 가상의 사용자
        self.user_kim = User.objects.create_user(username="kim", password="somepassword") #포스트목록페이지에 작성자 추가하기
        self.user_lee = User.objects.create_user(username="lee", password="somepassword")

        self.category_com = Category.objects.create(name="computer", slug="computer") #Category 레코드 두개 만들기
        self.category_edu = Category.objects.create(name="education", slug="education")

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.user_kim, category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.", author=self.user_lee, category=self.category_edu)
        self.post_002 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다.", author=self.user_lee)

    def nav_test(self, soup):
        navbar = soup.nav  # <nav></nav>사이의 html문서 navbar가 정상적으로 보이는지

        #navbar의 텍스트 중 Blog와 About me 있는지 확인
        # self.assertIn('Blog', soup.nav.text)
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', soup.nav.text)

        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_btn = navbar.find('a', text="About Me")
        self.assertEqual(about_btn.attrs['href'], '/about_me/')

    def category_test(self, soup):
        category_card = soup.find('div', id='category_card')
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com.name} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_edu.name} ({self.category_edu.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)


    def test_post_list(self):
        # self.assertEqual(3, 3)
        
        #포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/', follow=True)   #301오류날시 follw=True 추가
        
        # response 결과가 정상적으로 보이는지, 정상적으로 페이지 로드
        self.assertEqual(response.status_code, 200) # 성공적으로 결과를 돌려줄땐 200, 서버에서 요청한 페이지를 찾을 수 없을 때 404반환

        # title이 정상적으로 보이는지
        soup = BeautifulSoup(response.content, 'html.parser') #BeautifulSoup로 읽어드리고, html.parser로 파싱한 결과를 soup에 담음
        self.assertEqual(soup.title.text, 'Blog')   #title요소에서 .text로 텍스트가 같은지 비교


        self.nav_test(soup)
        self.category_test(soup)

        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

        # post가 정상적으로 보이는지
        # 1. 맨 처음엔 Post가 없음
        # 2. Post가 추가
        # post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.user_kim) #포스트목록페이지에 작성자 추가하기
        # post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.", author=self.user_lee)

        #포스트가 없는경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        #포스트 목록페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        #포스트가 하나 있다.
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.user_kim) #admin에 저장x. test실행 시 잠깐 생겼다가 사라짐 #포스트목록페이지에 작성자 추가하기
        
        #그 포스트의 url은 'blog/1/'이다
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')
        
        #첫번째페이지의 상세페이지 테스트
        #첫 번째 post url로 접근하면 정상적으로 작동
        response = self.client.get(self.post_001.get_absolute_url(), follow=True) # '/blog/1/'
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # navbar가 정상적으로 보이는지
        self.nav_test(soup)
        
        #첫번째 포스트 제목이 웹 브라우저 탭 타이플에 들어있다.
        self.assertIn(self.post_001.title, soup.title.text)
        
        #첫번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        #첫번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
        # 첫번째 포스트의 작성자 포스트 영역에 있다.
        self.assertIn(self.post_001.author.username.upper(), post_area.text) #포스트상세페이지에 작성자 추가하기
