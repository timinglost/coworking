from django.shortcuts import render

def main(request):
    title = 'Контакты'


    context = {
        'title': title,
    }
    return render(request, 'feedbackapp/pages-contact.html', context)


def questions(request):
    title = 'F.A.Q.'


    context = {
        'title': title,
    }
    return render(request, 'feedbackapp/pages-faq.html', context)


def question(request):
    title = 'F.A.Q.'


    context = {
        'title': title,
    }
    return render(request, 'feedbackapp/question.html', context)