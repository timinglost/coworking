from django.shortcuts import render

def main(request):
    title = 'Pages / Contact - NiceAdmin Bootstrap Template'


    context = {
        'title': title,
    }
    return render(request, 'feedbackapp/pages-contact.html', context)
