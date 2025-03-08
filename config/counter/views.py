from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import re


def load_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name

        fs = FileSystemStorage()
        fs.save(file_name, uploaded_file)

        file_path = fs.path(file_name)

        encodings = ['utf-8', 'windows-1251', 'latin-1', 'utf-16', 'ISO-8859-1']
        file_content = None

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    file_content = file.read()
                break
            except (UnicodeDecodeError, FileNotFoundError) as e:
                continue

        if file_content is None:
            return HttpResponse("Ошибка при чтении файла. Пожалуйста, убедитесь, что файл в правильной кодировке.",
                                status=400)

        words_in_file = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]+\b', file_content.lower())

        return render(request, 'upload.html', {'words_in_file': words_in_file})

    return render(request, 'upload.html')


def word_count(request):
    count = 0
    word_to_count = None
    if request.method == 'POST':
        word_to_count = request.POST.get('word')
        if word_to_count:
            word_to_count = word_to_count.lower()
            if 'words_in_file' in request.session:
                count = request.session['words_in_file'].count(word_to_count)

    return render(request, 'upload.html', {'word_to_count': word_to_count, 'count': count})


def clear_memory(request):
    if 'words_in_file' in request.session:
        del request.session['words_in_file']
    return render(request, 'upload.html', {'word_to_count': None, 'count': 0})
