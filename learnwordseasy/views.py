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


def repeat(words):
    global col
    words = Words.objects.all()
    for word in words:
        col += 1

    if col <= int(len(words)):
        return
    else:
        choose_word(words)


def start_test(request):
    a = 0
    words = Words.objects.all()
    # news = News.objects.filter(category_id=category_id)
    # category = Category.objects.get(pk=category_id)
    num_side = random.randint(1, 2)
    word_id = choose_word(words)
    """
    list_of_words = []
    for word in words:
        list_of_words.append(word.title1)
    random.shuffle(list_of_words)
    q_word = list_of_words[a]
    word_id = Words.objects.filter(title1=q_word)
    get_first_of_word = word_id.first()
    get_for_test = get_first_of_word.for_test
    if int(get_for_test) == 0:
        word_id.update(for_test=1)
    elif int(get_for_test) == 1:
        word_id.update(for_test=2)
    elif int(get_for_test) == 2:
        word_id.update(for_test=3)
    elif int(get_for_test) == 3:
        word_id.update(for_test=4)
    else:
        a = int(get_for_test)
        repeat(a)
    """

    return render(request, 'learnwordseasy/index2.html', {
        'num_side': num_side,
        'words': words,
        'word_id': word_id,

    })


def choose_word(words):
    words = Words.objects.all()
    list_of_words = []
    for word in words:
        list_of_words.append(word.title1)
    random.shuffle(list_of_words)
    q_word = list_of_words[0]
    word_id = Words.objects.filter(title1=q_word)
    get_first_of_word = word_id.first()
    get_for_test = get_first_of_word.for_test
    if int(get_for_test) == 0:
        word_id.update(for_test=1)
        return word_id
    elif int(get_for_test) == 1:
        word_id.update(for_test=2)
        return word_id
    elif int(get_for_test) == 3:
        repeat(words)
    elif int(get_for_test) == 2:
        word_id.update(for_test=3)
        return word_id



