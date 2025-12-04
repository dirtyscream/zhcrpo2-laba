from django.http import Http404, FileResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import pin
import random
from io import BytesIO

words = ['be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want', 'give',
         'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call']

class PasteView:
    def index(request):
        if request.method == 'POST':
            text = request.POST['main_text']
            if text.strip() != '':
                slug = '-'.join(random.choices(words, k=3))
                while pin.objects.filter(slug=slug).exists() == True:
                    slug = '-'.join(random.choices(words, k=3))
                pin(text=text, slug=slug).save()
                return redirect('pin_preview', slug)

        return render(request, 'paste/index.html')

    def preview(request, pin_id):
        try:
            pin_responce = pin.objects.get(slug=pin_id)
        except:
            raise Http404()
        data = {
            'text': pin_responce.text,
            'date': pin_responce.date.strftime('%Y-%m-%d %H:%M:%S'),
            'slug': pin_id
        }
        return render(request, 'paste/preview.html', data)

    def download(request, pin_id):
        try:
            file = pin.objects.get(slug=pin_id)
        except:
            raise Http404()
        buffer = BytesIO()
        buffer.write(file.text.encode('utf-8'))
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'{pin_id}.txt')

    def delete(request, pin_id):
        try:
            if request.GET['93c5272130ea44dba67e8dcc0107b8f7'] == '14583209':
                pin.objects.get(slug=pin_id).delete()
        except:
            raise Http404()
        return HttpResponse('1')
