from views import normal_list, normal_word_form, create_random_number, creating_final_answers, shuffling_of_lists


def german_wrong_answer(true_answer):  # Функция для создания рандомных ответов на немецком
    list_words = normal_list("title1")  # вызываем функцию чтобы сразу получить слова в удобном виде
    true_look_answer = normal_word_form(true_answer,
                                        "title1")  # вызываем функ. чтобы получить правильный ответ в удобном виде

    list_words.remove(true_look_answer)  # удаляем правильный ответ так как может попасться такой же
    r_n = create_random_number(list_words)  # получаем 3 рандомных числа чтобы потом использовать как индексы
    q_transl = creating_final_answers(r_n, list_words, true_look_answer)  # создаем конечный выбор ответов
    q_transl = shuffling_of_lists(q_transl, 5)  # мешаем

    return q_transl


def russian_wrong_answer(true_answer):  # Функция для создания рандомных ответов на русском
    list_words = normal_list("title2")  # вызываем функцию чтобы сразу получить слова в удобном виде
    true_look_answer = normal_word_form(true_answer,
                                        "title2")  # вызываем функ. чтобы получить правильный ответ в удобном виде

    list_words.remove(
        true_look_answer)  # удаляем его чтобы не было повторений в ответах, ведь он может выскочить повторно
    r_n = create_random_number(list_words)  # получаем 3 рандомных числа чтобы потом использовать как индексы
    q_words = creating_final_answers(r_n, list_words, true_look_answer)  # создаем финальный список ответов
    q_words = shuffling_of_lists(q_words, 5)  # мешаем

    return q_words
