import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Words

col = 0


def index(request):
    words = Words.objects.all()  # Берем все слова из бд
    categories = Category.objects.all()  # Берем все категории из бд
    return render(request, 'learnwordseasy/index.html', {
        'words': words,
        'title': 'список слов',
        'categories': categories,
    })


"""
def repeat(words):
    global col
    words = Words.objects.all()
    for word in words:
        col += 1

    if col <= int(len(words)):
        return
    else:
        choose_word(words)
"""


def random_num2(true_answer):  # Функция для создания рандомных ответов на русском
    dop_list = Words.objects.values('title1')  # Собираем все слова на немецком
    list_word = []  # для удобства создаем список
    for i in range(0, len(dop_list)):
        s = dop_list[i]
        s = s["title1"]
        list_word.append(s)  # приводим слова в читаемую форму

    r_n = []
    q_transl = []

    a = true_answer.values("title1")
    a = a[0]
    a = a["title1"]  # приводим правильное слово в адекватную форму

    list_word.remove(a)  # удаляем правильный ответ чтобы не было одинаковых ответов
    q_transl.append(a)  # сразу добавим в конечный список

    len_list_word = len(list_word) - 1
    while len(r_n) != 3:  # начинаем добавлять
        num = random.randint(0, len_list_word)  # берем рандомное число
        if num not in r_n:  # смотрим входит ли число в количество элемнтов списка
            r_n.append(num)  # если есть значит добовляем в список рандомных чисел, и так 3 раза

    for num in r_n:  # перебор чисел
        q_transl.append(list_word[num])  # добавляем все слова с такими индексами

    for i in range(0, 5):  # рандомно 5 раз их мешаем для рандомности:_)
        random.shuffle(q_transl)

    return q_transl  # возвращаем


def random_num1(true_answer):  # Функция для создания рандомных ответов на немецком
    dop_list = Words.objects.values('title2')  # Берем все слова из бд
    list_word = []  # создаем список чтобы в него ложить слова в читаемой форме
    for i in range(0, len(dop_list)):
        s = dop_list[i]
        s = s["title2"]
        list_word.append(s)  # привом слова в нормальную форму и добавляем

    r_n = []
    q_transl = []

    a = true_answer.values("title2")
    a = a[0]
    a = a["title2"]  # приводим правильный ответ в читаемый

    list_word.remove(a)  # удаляем его чтобы не было повторений в ответах, ведь он может выскочить вторым
    q_transl.append(a)  # сразу добавляем ведь его уже нет в основном списке слов

    len_list_word = len(list_word) - 1
    while len(r_n) != 3:  # нам нужны 3 рандомных числа чтобы потом взять их как индексы слов
        num = random.randint(0, len_list_word)  # берем рандомное число
        if num not in r_n:  # если его нет ещё в нашем списке
            r_n.append(num)  # добавляем если такого ещё нет чтобы избежать повторений

    for num in r_n:
        q_transl.append(list_word[num])  # используем рандомные номера как индексы и создаем конечный список

    for i in range(0, 5):
        random.shuffle(q_transl)  # мешаем 5 раз :_)

    return q_transl


def start_test(request):
    global col
    list_of_translate = []  # создаем список если карточка будет стороной на русском
    words = Words.objects.filter(
        for_test__in=[0, 1, 2])  # берем слова из бд только те которые были показаны меньше 3 раз

    translate = Words.objects.values('title2')  # берем все слова переведенные чтобы потом передать в рандомайзер
    for i in range(0, len(translate)):
        s = translate[i]
        s = s["title2"]
        list_of_translate.append(s)  # приводим в адекватное состояние

    for i in range(0, 2):
        random.shuffle(list_of_translate)  # мешаем

    num_side = random.randint(1, 2)  # рандомно выбераем какой стороной будет наша карточка
    list_of_words = []  # создаем пустой список для слов
    for word in words:
        list_of_words.append(word.title1)  # добавляем все слова в читаемом виде

    random.shuffle(list_of_words)  # рандомно перемешиваем

    q_word = list_of_words[0]  # берем первое слово

    word_id = Words.objects.filter(title1=q_word)  # забираем всю инфу об этом слове
    get_first_of_word = word_id.first()  # берем его фирст
    get_for_test = get_first_of_word.for_test  # забираем его значение чтобы потом поменять

    # list_of_translate.remove(get_first_of_word.title2)
    if num_side == 1:  # если карточка первой стороной то ответы будут немецкими
        rand_answer = random_num1(word_id)  # передаем правильное слово
    else:
        rand_answer = random_num2(word_id)  # в другом случае на русском

    # далее мы меняем значение чтобы показывали 1 слово не более 3 раз
    if int(get_for_test) == 0:
        word_id.update(for_test=1)
    elif int(get_for_test) == 1:
        word_id.update(for_test=2)
    elif int(get_for_test) == 2:
        word_id.update(for_test=3)

    true_ans = word_id[0]  # берем правильное слово и передаем чтобы понять какое из них ответов оно

    return render(request, 'learnwordseasy/index2.html', {
        'num_side': num_side,
        # 'words': words,
        'word_id': word_id,
        # 'translate': list_of_translate,
        'word1': rand_answer[0],
        'word2': rand_answer[1],
        'word3': rand_answer[2],
        'word4': rand_answer[3],
        'true_ans': true_ans

    })


def check_for_test(): # функция чтобы понять нужно ли запускать следующий тест или есть ещё слова которые можно показать
    words = Words.objects.filter(for_test__in=[0, 1, 2]) # берем все допустимые для показа слова
    if len(words) == 0: # если таких нет то отправляем флажок что пора брать новый тест
        return 1
    else: # в другом случае продолжаем
        return 2


def get_answer(request): # Проверка Правильности слова
    answer = request.POST.get("answer", "Undefined")  # получаем ответ пользователя
    side = request.POST.get("side", "Undefined")  # получаем на каком языке написано задаваемое слово
    true_an = request.POST.get("true_an", "Undefined")  # получаем правильный ответ
    if int(side) == 1:  # если вопрос на русском
        words = Words.objects.filter(title1=true_an)  # находим всю инфу про слово-ответ
        get_first_of_word = words.first()  # берем его информацию
        get_title2 = get_first_of_word.title2  # забираем перевод
        if answer == get_title2:  # если ответ правильный
            result = "Ответ ПРАВИЛЬНЫЙ!!!!"
        else:  # в другом случаем
            result = "ПОКА Ответ ПРАВИЛЬНЫЙ ТЫ ДИБИЛ!!!!"

    elif int(side) == 2:  # если вопрос на немецком
        words = Words.objects.filter(title1=true_an)  # находим всю инфу про слово-ответ
        get_first_of_word = words.first()  # берем его информацию
        get_title2 = get_first_of_word.title1  # забираем
        if answer == get_title2:  # если ответ правильный
            result = "Ответ ПРАВИЛЬНЫЙ!!!!"
        else:  # в другом случаем
            result = "ПОКА Ответ ПРАВИЛЬНЫЙ ТЫ ДИБИЛ!!!!"

    next = check_for_test()

    return render(request, "learnwordseasy/perebivka.html", {
        'answer': answer,
        'words': get_title2,
        'true_an': true_an,
        'side': side,
        'result': result,
        'next': next,
    })


def wort_in_words(request):
    return render(request, 'learnwordseasy/wortinword.html')
