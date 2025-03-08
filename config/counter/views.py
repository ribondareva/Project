import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


def load_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name

        fs = FileSystemStorage()
        fs.save(file_name, uploaded_file)

        encodings = ['utf-8', 'windows-1251', 'latin-1', 'utf-16', 'ISO-8859-1']
        file_content = None

        for encoding in encodings:
            try:
                with open(fs.path(file_name), 'r', encoding=encoding) as file:
                    file_content = file.read()
                break
            except (UnicodeDecodeError, FileNotFoundError):
                continue

        if file_content is None:
            return HttpResponse("Ошибка при чтении файла. Проверьте кодировку.", status=400)

        words_in_file = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]+\b', file_content.lower())

        request.session['words_in_file'] = words_in_file
        request.session.modified = True

        print("Загруженные слова:", words_in_file)  # Отладка в консоли

        return render(request, 'upload.html', {'file_uploaded': True})

    return render(request, 'upload.html')


def word_count(request):
    count = 0
    word_to_count = None

    if request.method == 'POST':
        word_to_count = request.POST.get('word', '').strip().lower()

        words_in_file = request.session.get('words_in_file', [])

        print("Запрошенное слово:", word_to_count)  # Отладка
        print("Слова в сессии:", words_in_file[:20])

        count = words_in_file.count(word_to_count)

    return render(request, 'upload.html', {'word_to_count': word_to_count, 'count': count})


def clear_memory(request):
    request.session.pop('words_in_file', None)
    return render(request, 'upload.html', {'file_uploaded': False})
