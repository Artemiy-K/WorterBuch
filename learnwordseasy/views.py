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

def random_num(list_word, true_answer):
    r_n = []
    q_transl = []

    a = true_answer.values("title2")
    a = a[0]
    a = a["title2"]
    q_transl.append(a)

    for i in range(0, 3):
        num = random.randint(0, len(list_word))
        r_n.append(num)

    for num in r_n:
        if list_word[num] != a:
            q_transl.append(list_word[num])

    return q_transl


def start_test(request):
    global col
    list_of_translate = []
    words = Words.objects.filter(for_test__in=[0,1,2])

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

    rand_trans = random_num(list_of_translate, word_id)

    if int(get_for_test) == 0:
        word_id.update(for_test=1)
    elif int(get_for_test) == 1:
        word_id.update(for_test=2)
    elif int(get_for_test) == 3:
        return
    elif int(get_for_test) == 2:
        word_id.update(for_test=3)

    return render(request, 'learnwordseasy/index2.html', {
        'num_side': num_side,
        'words': words,
        'word_id': word_id,
        'translate': list_of_translate,
        'rand_trans': rand_trans

    })
