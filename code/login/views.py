from django.shortcuts import redirect, render
from django.http import HttpResponse

class LoginView:
    def index(request):
        return redirect('pin/create')

    def login(request):
        data = {}
        try:
            sess_id = request.session.get(request.GET['q'], '')
            if sess_id != '':
                data['error'] = sess_id
                del request.session[request.GET['q']]
            else:
                return redirect('/login/')
        except:
            pass

        return render(request, 'login/index.html',data)


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
