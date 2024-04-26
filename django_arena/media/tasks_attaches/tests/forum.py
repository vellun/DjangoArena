import django.test
import http
import answers


class RedirectUserTests(django.test.TestCase):
    def check_redirect(self):
        response1 = answers.forum.Solution().get()
        url = "https://django.forum2x2.ru/"
        response = django.test.Client().get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response1.status_code, response.status_code)

