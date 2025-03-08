import re
from django.shortcuts import render
from .forms import FileUploadForm, WordCountForm

# Для хранения данных о словах используем глобальную переменную
words = []


# Загрузка файла
def load_file(file):
    global words
    text = file.read().decode('utf-8')
    # Находим все буквенные слова и приводим их к нижнему регистру
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())


# Подсчет слов
def word_count(word):
    global words
    return words.count(word.lower())


# Главная страница с формами
def index(request):
    global words
    word_count_result = None
    if request.method == 'POST':
        if 'load' in request.POST:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                load_file(file)
                return render(request, 'counter/index.html',
                              {'form': form, 'word_count_form': WordCountForm(), 'message': 'Файл загружен',
                               'words': words})

        elif 'wordcount' in request.POST:
            form = WordCountForm(request.POST)
            if form.is_valid():
                word = form.cleaned_data['word']
                word_count_result = word_count(word)
                return render(request, 'counter/index.html', {'form': FileUploadForm(), 'word_count_form': form,
                                                              'word_count_result': word_count_result, 'words': words})

        elif 'clear' in request.POST:
            words = []
            return render(request, 'counter/index.html',
                          {'form': FileUploadForm(), 'word_count_form': WordCountForm(), 'message': 'Память очищена',
                           'words': words})
    else:
        form = FileUploadForm()
        word_count_form = WordCountForm()

    return render(request, 'counter/index.html', {'form': form, 'word_count_form': word_count_form, 'words': words})
