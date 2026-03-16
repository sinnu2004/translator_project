from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class TranslatorViewGETTest(TestCase):
    """Test that the home page loads correctly."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    def test_home_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "main/index.html")

    def test_home_contains_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, "<form")

    def test_home_contains_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_home_contains_language_dropdown(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'name="language"')

    def test_home_contains_translate_input(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'name="translate"')

    def test_home_lists_all_20_languages(self):
        response = self.client.get(self.url)
        languages = response.context["languages"]
        self.assertEqual(len(languages), 20)

    def test_no_translation_on_get(self):
        response = self.client.get(self.url)
        self.assertIsNone(response.context["translated_text"])


class TranslatorViewPOSTTest(TestCase):
    """Test POST requests with mocked GoogleTranslator so no real API is called."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    @patch("main.views.GoogleTranslator")
    def test_post_returns_200(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "नमस्ते"
        response = self.client.post(self.url, {"translate": "Hello", "language": "hi"})
        self.assertEqual(response.status_code, 200)

    @patch("main.views.GoogleTranslator")
    def test_translation_appears_in_context(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "नमस्ते दुनिया"
        response = self.client.post(self.url, {"translate": "Hello World", "language": "hi"})
        self.assertEqual(response.context["translated_text"], "नमस्ते दुनिया")

    @patch("main.views.GoogleTranslator")
    def test_input_text_echoed_in_context(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "Hallo"
        response = self.client.post(self.url, {"translate": "Hello", "language": "de"})
        self.assertEqual(response.context["input_text"], "Hello")

    @patch("main.views.GoogleTranslator")
    def test_selected_language_echoed_in_context(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "Bonjour"
        response = self.client.post(self.url, {"translate": "Hello", "language": "fr"})
        self.assertEqual(response.context["selected_language"], "fr")

    @patch("main.views.GoogleTranslator")
    def test_translator_called_with_correct_language(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "Hola"
        self.client.post(self.url, {"translate": "Hello", "language": "es"})
        mock_translator_class.assert_called_once_with(source="auto", target="es")

    @patch("main.views.GoogleTranslator")
    def test_translator_called_with_correct_text(self, mock_translator_class):
        mock_instance = mock_translator_class.return_value
        mock_instance.translate.return_value = "Ciao"
        self.client.post(self.url, {"translate": "Hello", "language": "it"})
        mock_instance.translate.assert_called_once_with("Hello")

    @patch("main.views.GoogleTranslator")
    def test_translation_rendered_in_html(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "Merhaba"
        response = self.client.post(self.url, {"translate": "Hello", "language": "tr"})
        self.assertContains(response, "Merhaba")

    def test_empty_text_skips_translation(self):
        response = self.client.post(self.url, {"translate": "   ", "language": "hi"})
        self.assertIsNone(response.context["translated_text"])

    def test_missing_text_field_skips_translation(self):
        response = self.client.post(self.url, {"language": "hi"})
        self.assertIsNone(response.context["translated_text"])


class TranslatorErrorHandlingTest(TestCase):
    """Test how the app handles translator failures."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    @patch("main.views.GoogleTranslator")
    def test_translator_exception_shown_in_context(self, mock_translator_class):
        mock_translator_class.return_value.translate.side_effect = Exception("Network error")
        response = self.client.post(self.url, {"translate": "Hello", "language": "hi"})
        self.assertIn("Translation error", response.context["translated_text"])

    @patch("main.views.GoogleTranslator")
    def test_translator_exception_does_not_crash(self, mock_translator_class):
        mock_translator_class.return_value.translate.side_effect = Exception("Timeout")
        response = self.client.post(self.url, {"translate": "Hello", "language": "hi"})
        self.assertEqual(response.status_code, 200)

    @patch("main.views.GoogleTranslator")
    def test_error_message_rendered_in_html(self, mock_translator_class):
        mock_translator_class.return_value.translate.side_effect = Exception("API down")
        response = self.client.post(self.url, {"translate": "Hello", "language": "hi"})
        self.assertContains(response, "Translation error")


class TranslatorLanguageSupportTest(TestCase):
    """Test all 20 languages are accepted and forwarded correctly."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    @patch("main.views.GoogleTranslator")
    def test_all_languages_accepted(self, mock_translator_class):
        language_codes = [
            "hi", "mr", "de", "fr", "es", "ar", "zh-CN",
            "ja", "ko", "pt", "ru", "it", "tr", "nl",
            "pl", "sv", "ur", "bn", "ta", "te",
        ]
        for code in language_codes:
            mock_translator_class.return_value.translate.return_value = "test"
            response = self.client.post(self.url, {"translate": "Hello", "language": code})
            with self.subTest(language=code):
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context["translated_text"], "test")


class TranslatorAjaxEndpointTest(TestCase):
    """Test the /translate/ AJAX endpoint."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("translate_ajax")

    @patch("main.views.GoogleTranslator")
    def test_ajax_post_returns_json(self, mock_translator_class):
        mock_translator_class.return_value.translate.return_value = "こんにちは"
        response = self.client.post(self.url, {"translate": "Hello", "language": "ja"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("translation", data)
        self.assertEqual(data["translation"], "こんにちは")

    @patch("main.views.GoogleTranslator")
    def test_ajax_empty_text_returns_400(self, mock_translator_class):
        response = self.client.post(self.url, {"translate": "", "language": "hi"})
        self.assertEqual(response.status_code, 400)

    @patch("main.views.GoogleTranslator")
    def test_ajax_error_returns_500(self, mock_translator_class):
        mock_translator_class.return_value.translate.side_effect = Exception("Fail")
        response = self.client.post(self.url, {"translate": "Hello", "language": "hi"})
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())

    def test_ajax_get_request_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)