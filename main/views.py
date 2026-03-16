from django.shortcuts import render
from django.http import JsonResponse
from deep_translator import GoogleTranslator

LANGUAGES = [
    ("hi", "Hindi"),
    ("mr", "Marathi"),
    ("de", "German"),
    ("fr", "French"),
    ("es", "Spanish"),
    ("ar", "Arabic"),
    ("zh-CN", "Chinese"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
    ("pt", "Portuguese"),
    ("ru", "Russian"),
    ("it", "Italian"),
    ("tr", "Turkish"),
    ("nl", "Dutch"),
    ("pl", "Polish"),
    ("sv", "Swedish"),
    ("ur", "Urdu"),
    ("bn", "Bengali"),
    ("ta", "Tamil"),
    ("te", "Telugu"),
]

def home(request):
    context = {
        "languages": LANGUAGES,
        "translated_text": None,
        "input_text": "",
        "selected_language": "hi",
    }

    if request.method == "POST":
        text = request.POST.get("translate", "").strip()
        language_code = request.POST.get("language", "hi")

        if text:
            try:
                translation = GoogleTranslator(source="auto", target=language_code).translate(text)
                context["translated_text"] = translation
            except Exception as e:
                context["translated_text"] = f"Translation error: {str(e)}"

        context["input_text"] = text
        context["selected_language"] = language_code

    return render(request, "main/index.html", context)


def translate_ajax(request):
    if request.method == "POST":
        text = request.POST.get("translate", "").strip()
        language_code = request.POST.get("language", "hi")

        if not text:
            return JsonResponse({"error": "No text provided"}, status=400)

        try:
            translation = GoogleTranslator(source="auto", target=language_code).translate(text)
            return JsonResponse({"translation": translation})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)