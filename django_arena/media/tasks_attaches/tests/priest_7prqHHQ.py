import django.test
import core.models
import answers


class PriestTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = core.models.User.objects.create(
            username="Chipi",
            password="qazwsxedc12",
        )

    def request_priest(self):
        response = answers.priest.Solution().request()
        response1 = answers.priest.Solution().request()
        self.assertNotEqual(response, response1)
