import os
import re

from django.shortcuts import render
from django.http import HttpResponse
from .models import Word
from django.core.files.storage import FileSystemStorage


def load_file(request):
    word_count = None  # Переменная для хранения подсчета слов, если нужно отобразить результат

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Попробуем декодировать файл с несколькими кодировками
        try:
            file_content = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            uploaded_file.seek(0)  # Сбрасываем указатель на начало файла
            file_content = uploaded_file.read().decode('windows-1251', errors='ignore')  # Попробуем с другой кодировкой

        # Разбиваем текст на слова и фильтруем только буквенные
        words = re.findall(r'\b[a-zA-Z]+\b', file_content.lower())

        # Добавление или обновление слов в базе данных
        for word in words:
            obj, created = Word.objects.get_or_create(word=word)
            if not created:
                obj.count += 1
                obj.save()

        # Подсчитываем количество уникальных слов
        word_count = len(words)

        return render(request, 'upload.html', {'word_count': word_count})

    return render(request, 'upload.html', {'word_count': word_count})  # Отображаем страницу с результатами


def clear_memory(request):
    Word.objects.all().delete()  # Удаляем все записи в таблице Word
    return render(request, 'upload.html', {'unique_word_count': 0})
