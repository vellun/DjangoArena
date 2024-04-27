import http
import django.test
import django.urls


class StaticURLTests(django.test.TestCase):
    def test_item_list_endpoint(self):
        resp = django.test.Client().get(
            django.urls.reverse("~~~"),
        )
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    
    def test_item_endpoint(self):
        resp = django.test.Client().get(
            django.urls.reverse("~~~"),
        )
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    
    def test_list_endpoint(self):
        resp = django.test.Client().get(
            django.urls.reverse("~~~"),
        )
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
