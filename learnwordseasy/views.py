import random
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
    num_side = []
    s = []
    for word in words:
        s.append(word.title1)
        s.append(random.randint(1,2))
        num_side.append(s)
        s = []
    random.shuffle(num_side)
    return render(request, 'learnwordseasy/index2.html', {
        'words': words,
        'num_side': num_side,
    })
