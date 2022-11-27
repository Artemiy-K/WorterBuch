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


# нам нужны рандомные числа чтобы потом их использовать как индексы в списке и таким макаром получить рандомные ответы
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


def german_wrong_answer(true_answer):  # Функция для создания рандомных ответов на немецком
    list_word = normal_list("title1")  # вызываем функцию чтобы сразу получить слова в удобном виде
    true_look_answer = normal_word_form(true_answer,
                                        "title1")  # вызываем функ. чтобы получить правильный ответ в удобном виде

    list_word.remove(true_look_answer)  # удаляем правильный ответ так как может попасться такой же
    r_n = create_random_number(list_word)  # получаем 3 рандомных числа чтобы потом использовать как индексы
    q_transl = creating_final_answers(r_n, list_word, true_look_answer)  # создаем конечный выбор ответов
    q_transl = shuffling_of_lists(q_transl, 5)  # мешаем

    return q_transl


def russian_wrong_answer(true_answer):  # Функция для создания рандомных ответов на русском
    list_word = normal_list("title2")  # вызываем функцию чтобы сразу получить слова в удобном виде
    r_n = []
    true_look_answer = normal_word_form(true_answer,
                                        "title2")  # вызываем функ. чтобы получить правильный ответ в удобном виде

    list_word.remove(
        true_look_answer)  # удаляем его чтобы не было повторений в ответах, ведь он может выскочить повторно
    r_n = create_random_number(list_word)  # получаем 3 рандомных числа чтобы потом использовать как индексы
    q_words = creating_final_answers(r_n, list_word, true_look_answer)  # создаем финальный список ответов
    q_words = shuffling_of_lists(q_words, 5)  # мешаем

    return q_words


def get_info_about_word(title1_of_word):  # забираем всю инфу из бд об этом слове
    word_id = Words.objects.filter(title1=title1_of_word)
    get_first_of_word = word_id.first()
    return get_first_of_word


def start_test(request):
    # list_of_translate = []  # создаем список если карточка будет стороной на русском
    words = Words.objects.filter(
        for_test__in=[0, 1, 2])  # берем слова из бд только те которые были показаны меньше 3 раз

    num_side = random.randint(1, 2)  # рандомно выбераем какой стороной будет наша карточка
    list_of_words = []
    for word in words:
        list_of_words.append(word.title1)  # добавляем все слова в читаемом виде

    list_of_words = shuffling_of_lists(list_of_words, 2)  # рандомно перемешиваем
    q_word = list_of_words[0]  # берем первое слово

    get_for_test = get_info_about_word(q_word).for_test  # забираем его значение чтобы потом поменять

    word_id = Words.objects.filter(title1=q_word)
    if num_side == 1:  # если карточка первой стороной то ответы будут русском
        rand_answer = russian_wrong_answer(word_id)  # передаем правильное слово
    else:  # в другом случае на немецком
        rand_answer = german_wrong_answer(word_id)  # передаем правильное слово

    # далее мы меняем значение чтобы показывали 1 слово не более 3 раз
    if int(get_for_test) == 0:
        word_id.update(for_test=1)
    elif int(get_for_test) == 1:
        word_id.update(for_test=2)
    elif int(get_for_test) == 2:
        word_id.update(for_test=3)

    true_ans = word_id[0]  # берем правильное слово и передаем чтобы понять какой из ответов правильный

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
    if int(side) == 1:  # если вопрос на русском # берем его информацию
        get_title_word = get_info_about_word(true_an).title2  # забираем перевод
        if answer == get_title_word:  # если ответ правильный
            resultt = "Ответ ПРАВИЛЬНЫЙ!!!!"
        else:
            resultt = "ПОКА Ответ не ПРАВИЛЬНЫЙ ТЫ ДИБИЛ!!!!"

    elif int(side) == 2:  # если вопрос на немецком берем его информацию
        get_title_word = get_info_about_word(true_an).title1  # забираем
        if answer == get_title_word:  # если ответ правильный
            resultt = "Ответ ПРАВИЛЬНЫЙ!!!!"
        else:
            resultt = "ПОКА Ответ не ПРАВИЛЬНЫЙ ТЫ ДИБИЛ!!!!"

    next_q = check_for_test()  # смотрим не пора ли уже менять тест ведь слова могут закончиться

    return render(request, "learnwordseasy/perebivka.html", {
        'answer': answer,
        'words': get_title_word,
        'true_an': true_an,
        'side': side,
        'result': resultt,
        'next': next_q,
    })


# функция чтобы вытянуть из бд пример применения слова
def get_example(word):
    num_of_example = random.randint(1, 3)  # рандомное число
    if num_of_example == 1:
        word_info = get_info_about_word(word).example1
    elif num_of_example == 2:
        word_info = get_info_about_word(word).example2
    else:
        word_info = get_info_about_word(word).example3
    return word_info  # и вытягиваем один из примеров


def character_count_leave(word):
    if len(word) < 4:
        character_leave = 2
    elif len(word) >= 4 and len(word) <= 6:
        character_leave = 3
    else:
        character_leave = int(len(word)) // 2 + 1

    return character_leave


def add_word_inlist(word):
    word_in_list = []
    for i in range(0, len(word)):
        word_in_list.append(word[i])
    return word_in_list


def dropping_letters(word):
    letters = []
    word_in_list = add_word_inlist(word)
    # word_in_list2 = add_word_inlist(word)
    count_of_letter = character_count_leave(word)
    # chek_repeated_words = False

    while len(letters) != count_of_letter:
        true_len_word = len(word_in_list) - 1
        num_letter = random.randint(0, true_len_word)
        if num_letter not in letters:
            letters.append(num_letter)
            word_in_list.remove(word_in_list[num_letter])
    """
    chek_bug = add_word_inlist(word)
    for item in chek_bug:
        if int(chek_bug.count(item)) == 2:
            rand = random.randint(1, 2)
            if int(rand) == 1:
                letters.remove(item)
            else:
                letters.append(item)
    """
    # spare_wil = list(word_in_list)

    # for item in spare_wil:
    # if item in word_in_list2:
    # if spare_wil.count(item) < word_in_list2.count(item):
    # spare_wil.append(item)

    letters.sort()

    return word_in_list, letters  # , spare_wil


def correction_translate(example, translate, word):
    example_list = example.replace(".", "").replace("-", "").replace("!", "").replace("(", "").replace(")", "").replace(
        ",", "").replace("?", "").replace(":", "").replace(";", "").split(' ')

    for item in example_list:
        if item.capitalize() == word.capitalize():
            index_word = example_list.index(item)
            example_list.remove(item)
            example_list.insert(index_word, translate)

    end_str = ''
    for item in example_list:
        end_str += ' ' + item

    return end_str


def wort_in_words(request):
    words = Words.objects.filter(for_test__in=[3])  # берем все допустимые слова

    list_of_words = []
    for word in words:
        list_of_words.append(word.title1)  # добавляем все слова в читаемом виде

    list_of_words = shuffling_of_lists(list_of_words, 4)  # мешаем

    first_word = Words.objects.get(title1=list_of_words[0])  # получаем инфу о слове
    category_of_word = first_word.category  # получаем его категорию чтобы понять есть ли артикль
    get_translate = first_word.title2
    first_word = first_word.title1  # получаем его название на немецком
    get_example_word = get_example(first_word)  # вызываем его пример применнения

    if str(category_of_word) == "Substantiv":  # если сущ значит убераем артикль
        first_word = first_word[4:]

    tru_example = correction_translate(get_example_word, get_translate, first_word)

    list_with_letter = dropping_letters(first_word)

    word_in_list = add_word_inlist(first_word)

    return render(request, 'learnwordseasy/wortinword.html', {
        'words': first_word,
        'letter': list_with_letter[0],
        'get_example_word': tru_example,
        'word_in_list': word_in_list,
        'get_translate': get_translate
    })


def check_bug(word_in_list, list_with_letter):
    comparison_list = []
    not_more_one = True

    for item in word_in_list:
        not_more_one = True
        for item2 in list_with_letter:
            if item == item2:
                if not_more_one:
                    comparison_list.append(item)
                    not_more_one = False

    if comparison_list == list_with_letter:
        return True
    else:
        return False


def verification(request):
    input_list = []
    # letter_answer = request.POST.get("letter_answer", "Undefined")
    word_in_list = request.POST.get("word_in_list", "Undefined")
    # proper_word = request.POST.get("proper_word", "Undefined")
    len_list = len(word_in_list) - 1
    for i in range(0, len_list):
        s = request.POST.get(str(i), "Undefined")
        if s != "Undefined":
            input_list.append(s.lower())

    letter = request.POST.get("letter", "Undefined").replace('[', '').replace(']', '').replace(',', '').replace('\'',
                                                                                                                '').lower().split(
        " ")

    word_in_list = word_in_list.replace('[', '').replace(']', '').replace(',', '').replace('\'', '').lower().split(" ")

    mixing_check = check_bug(word_in_list, input_list)

    if not mixing_check:
        result = 'ты дебил не правильно'
        return render(request, 'learnwordseasy/perebivka2.html', {
            'answer': input_list,
            'answer2': letter,
            'answ3': word_in_list,
            'result': result
        })

    input_list = [j for i in [input_list, letter] for j in i]

    if len(word_in_list) > len(input_list):
        for item in input_list:
            if item in word_in_list:
                if word_in_list.count(item) > input_list.count(item):
                    while word_in_list.count(item) != input_list.count(item):
                        input_list.append(item)

    if sorted(word_in_list) == sorted(input_list):
        result = "Всё правильно молодец!"
    else:
        result = 'ты дебил не правильно'

    return render(request, 'learnwordseasy/perebivka2.html', {
        'answer': input_list,
        'answer2': letter,
        'answ3': word_in_list,
        'result': result
    })
