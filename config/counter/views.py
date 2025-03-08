import re

from django.shortcuts import render
from .models import Word


def load_file(request):
    word_count = None

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            file_content = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            file_content = uploaded_file.read().decode('windows-1251', errors='ignore')

        words = re.findall(r'\b[a-zA-Z]+\b', file_content.lower())

        for word in words:
            obj, created = Word.objects.get_or_create(word=word)
            if not created:
                obj.count += 1
                obj.save()

        word_count = len(words)

        return render(request, 'upload.html', {'word_count': word_count})

    return render(request, 'upload.html', {'word_count': word_count})


def clear_memory(request):
    Word.objects.all().delete()
    return render(request, 'upload.html', {'unique_word_count': 0})
