from django.shortcuts import render

def main(request):
    title = 'Контакты'


    context = {
        'title': title,
    }
    return render(request, 'feedbackapp/pages-contact.html', context)


def questions(request):
    title = 'Вопросы'


    context = {
        'title': title,
    }
    return render(request, 'feedbackapp/pages-faq.html', context)