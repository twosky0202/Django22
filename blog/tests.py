from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # self.assertEqual(3, 3)
        response = self.client.get('/blog/', follow=True)   #301오류날시 follw=True 추가
        # response 결과가 정상적으로 보이는지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')   #.text로 텍스트가 같은지 비교

        # navbar가 정상적으로 보이는지
        navbar = soup.nav   #<nav></nav>사이의 html문서
        # self.assertIn('Blog', soup.nav.text)
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', soup.nav.text)

        # post가 정상적으로 보이는지
        # 1. 맨 처음엔 Post가 없음
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        #2. Post가 추가
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.")
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)