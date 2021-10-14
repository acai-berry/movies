from django.shortcuts import render

from movies_app.models import Genre, Film


# Create your views here.
def test(request):
    data = Film.objects.all()
    films = {'films': data}
    return render(request, 'index.html', films)
