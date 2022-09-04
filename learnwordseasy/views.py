import random
from random import randint
from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Words


def index(request):
    words = Words.objects.all()
    categories = Category.objects.all()
    return render(request, 'learnwordseasy/index.html', {
        'words': words,
        'title': 'список слов',
        'categories': categories,
    })

def start_test(request):
    words = Words.objects.all()
    n = []
    s = []
    for word in words:
        s.append(word)
        s.append(random.randint(1,2))
        n.append(s)
        s = []
    rand_num = random.randint(1, len(n))
    return render(request, 'learnwordseasy/index2.html', {
        'words': words,
        'rand_num': rand_num,
        'n': n,
    })
