import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Words

col = 0


# dop_list = []

def index(request):
    words = Words.objects.all()
    categories = Category.objects.all()
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


def random_num2(list_word, true_answer):
    r_n = []
    q_transl = []

    a = true_answer.values("title1")
    a = a[0]
    a = a["title1"]

    list_word.remove(a)
    q_transl.append(a)

    len_list_word = len(list_word) - 1
    while len(r_n) != 3:
        num = random.randint(0, len_list_word)
        if num not in r_n:
            r_n.append(num)

    for num in r_n:
        q_transl.append(list_word[num])

    for i in range(0, 5):
        random.shuffle(q_transl)

    return q_transl


def random_num1(list_word, true_answer):
    r_n = []
    q_transl = []

    a = true_answer.values("title2")
    a = a[0]
    a = a["title2"]

    list_word.remove(a)
    q_transl.append(a)

    len_list_word = len(list_word) - 1
    while len(r_n) != 3:
        num = random.randint(0, len_list_word)
        if num not in r_n:
            r_n.append(num)

    for num in r_n:
        q_transl.append(list_word[num])

    for i in range(0, 5):
        random.shuffle(q_transl)

    return q_transl


def start_test(request):
    global col
    list_of_translate = []
    words = Words.objects.filter(for_test__in=[0, 1, 2])

    translate = Words.objects.values('title2')
    for i in range(0, len(translate)):
        s = translate[i]
        s = s["title2"]
        list_of_translate.append(s)

    for i in range(0, 2):
        random.shuffle(list_of_translate)
    # news = News.objects.filter(category_id=category_id)
    # category = Category.objects.get(pk=category_id)
    num_side = random.randint(1, 2)
    list_of_words = []
    for word in words:
        list_of_words.append(word.title1)

    random.shuffle(list_of_words)

    q_word = list_of_words[0]

    word_id = Words.objects.filter(title1=q_word)
    get_first_of_word = word_id.first()
    get_for_test = get_first_of_word.for_test

    # list_of_translate.remove(get_first_of_word.title2)
    if num_side == 1:
        rand_answer = random_num1(list_of_translate, word_id)
    else:
        rand_answer = random_num2(list_of_words, word_id)

    if int(get_for_test) == 0:
        word_id.update(for_test=1)
    elif int(get_for_test) == 1:
        word_id.update(for_test=2)
    elif int(get_for_test) == 2:
        word_id.update(for_test=3)

    true_ans = word_id[0]

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


def check_for_test():
    words = Words.objects.filter(for_test__in=[0, 1, 2])
    if len(words) == 0:
        return 1
    else:
        return 2


def get_answer(request):
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
