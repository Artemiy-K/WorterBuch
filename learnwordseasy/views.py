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


# преобразование слов в списке из <QuerySet [<Word: Das Buch>]> =>> в "Das Buch"
def normal_list(title):  # функция для того чтобы сделать слова в словаре в нормальном виде
    dop_list = Words.objects.values(
        title)  # Собираем все слова на выбранном языке взависимости title1 или title2 немецкий или русский
    list_word = []  # для удобства создаем список в котором будут конечные слова
    for i in range(0, len(dop_list)):
        s = dop_list[i]
        s = s[title]
        list_word.append(s)  # приводим слова в читаемую форму
    return list_word

"""
def normal_list(bad_list, title):  # функция для того чтобы сделать слова в словаре в нормальном виде
    # dop_list = Words.objects.values(title) Собираем все слова на выбранном языке взависимости title1 или title2 немецкий или русский
    list_word = []  # для удобства создаем список в котором будут конечные слова
    for i in range(0, len(bad_list)):
        s = bad_list[i]
        s = s[title]
        list_word.append(s)  # приводим слова в читаемую форму
    return list_word
"""

# преобразование правильного слова из <QuerySet [<Word: Fragen>]> =>> в "Fragen"
def normal_word_form(word, title):  # функция куда передаем само слово + title который определяет язык слова
    a = word.values(title)
    a = a[0]
    a = a[title]
    return a


# нам нужны рандомные числа чтобы потом их использовать как индексы и таким макаром получить рандомные ответы
def create_random_number(list_word):
    r_n = []
    len_list_word = len(list_word) - 1
    while len(r_n) != 3:  # нам нужны 3 рандомных числа чтобы потом взять их как индексы слов
        num = random.randint(0, len_list_word)  # берем рандомное число
        if num not in r_n:  # если его нет ещё в нашем списке рандомных чисел
            r_n.append(num)

    random.shuffle(r_n)  # перемешиваем его
    return r_n


def creating_final_answers(list_with_num, list_with_words, true_answer):
    q_words = []
    q_words.append(true_answer)  # cразу добавляем правильный ответ в конечный список
    for num in list_with_num:  # перебор чисел
        q_words.append(list_with_words[num])  # добавляем все слова с такими индексами

    return q_words


def shuffling_of_lists(your_list, time):  # перемешка элементов списка
    for i in range(0, time):
        random.shuffle(your_list)
    return your_list


def random_num2(true_answer):  # Функция для создания рандомных ответов на немецком
    list_word = normal_list("title1")  # вызываем функцию чтобы сразу получить слова в удобном виде
    true_look_answer = normal_word_form(true_answer,
                                        "title1")  # вызываем функ. чтобы получить правильный ответ в удобном виде

    list_word.remove(true_look_answer)  # удаляем правильный ответ так как может попасться такой же
    r_n = create_random_number(list_word)  # полчаем 3 рандомных числа чтобы потом использовать как индексы
    q_transl = creating_final_answers(r_n, list_word, true_look_answer)  # создаем конечный выбор ответов
    q_transl = shuffling_of_lists(q_transl, 5)  # мешаем

    return q_transl


def random_num1(true_answer):  # Функция для создания рандомных ответов на русском
    list_word = normal_list("title2")  # вызываем функцию чтобы сразу получить слова в удобном виде
    r_n = []
    true_look_answer = normal_word_form(true_answer,
                                        "title2")  # вызываем функ. чтобы получить правильный ответ в удобном виде

    list_word.remove(
        true_look_answer)  # удаляем его чтобы не было повторений в ответах, ведь он может выскочить повторно
    r_n = create_random_number(list_word)  # полчаем 3 рандомных числа чтобы потом использовать как индексы
    q_words = creating_final_answers(r_n, list_word, true_look_answer)  # создаем финальный список ответов
    q_words = shuffling_of_lists(q_words, 5)  # мешаем

    return q_words


def start_test(request):
    global col
    list_of_translate = []  # создаем список если карточка будет стороной на русском
    words = Words.objects.filter(
        for_test__in=[0, 1, 2])  # берем слова из бд только те которые были показаны меньше 3 раз



    num_side = random.randint(1, 2)  # рандомно выбераем какой стороной будет наша карточка
    list_of_words = []  # создаем пустой список для слов
    for word in words:
        list_of_words.append(word.title1)  # добавляем все слова в читаемом виде

    list_of_words = shuffling_of_lists(list_of_words, 2)  # рандомно перемешиваем
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


# функция чтобы понять нужно ли запускать следующий тест или есть ещё слова которые можно показать
def check_for_test():
    words = Words.objects.filter(for_test__in=[0, 1, 2])  # берем все допустимые для показа слова
    if len(words) == 0:  # если таких нет то отправляем флажок что пора брать новый тест
        return 1
    else:  # в другом случае продолжаем
        return 2


def get_answer(request):  # Проверка Правильности слова
    answer = request.POST.get("answer", "Undefined")  # получаем ответ пользователя
    side = request.POST.get("side", "Undefined")  # получаем на каком языке написано задаваемое слово
    true_an = request.POST.get("true_an", "Undefined")  # получаем правильный ответ
    if int(side) == 1:  # если вопрос на русском
        words = Words.objects.filter(title1=true_an)  # находим всю инфу про слово-ответ
        get_first_of_word = words.first()  # берем его информацию
        get_title_word = get_first_of_word.title2  # забираем перевод
        if answer == get_title_word:  # если ответ правильный
            resultt = "Ответ ПРАВИЛЬНЫЙ!!!!"
        else:  # в другом случаем
            resultt = "ПОКА Ответ ПРАВИЛЬНЫЙ ТЫ ДИБИЛ!!!!"

    elif int(side) == 2:  # если вопрос на немецком
        words = Words.objects.filter(title1=true_an)  # находим всю инфу про слово-ответ
        get_first_of_word = words.first()  # берем его информацию
        get_title_word = get_first_of_word.title1  # забираем
        if answer == get_title_word:  # если ответ правильный
            resultt = "Ответ ПРАВИЛЬНЫЙ!!!!"
        else:  # в другом случаем
            resultt = "ПОКА Ответ ПРАВИЛЬНЫЙ ТЫ ДИБИЛ!!!!"

    next_q = check_for_test() # смотрим не пора ли уже менять тест ведь слова могут закончиться

    return render(request, "learnwordseasy/perebivka.html", {
        'answer': answer,
        'words': get_title_word,
        'true_an': true_an,
        'side': side,
        'result': resultt,
        'next': next_q,
    })


def wort_in_words(request):
    l = ''
    words = Words.objects.filter(for_test__in=[3])
    categories = Category.objects.all()

    list_of_words = []  # создаем пустой список для слов
    for word in words:
        list_of_words.append(word.title1)  # добавляем все слова в читаемом виде

    list_of_words = shuffling_of_lists(list_of_words, 4)

    first_word = Words.objects.get(title1=list_of_words[0])
    category_of_word = first_word.category
    first_word = first_word.title1
    if str(category_of_word) == "Substantiv":
        first_word = first_word[3:]

    return render(request, 'learnwordseasy/wortinword.html', {
        'words': first_word,
        'categories': categories,
        'category_of_word': category_of_word,
    })
