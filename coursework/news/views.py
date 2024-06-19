from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView
# Create your views here.
def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article' #Ключ по которому мы передаём определённый объект внутрь шаблона

def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST) #Запрашиваем данные пользователя из формы
        if form.is_valid(): #Проверяем что данные корректно заполнены
            form.save() #Сохраням запись
            return redirect('/news') #Переадресация на страницу с новостями
        else:
            error = 'Введённая форма не верна'

    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'news/create.html', data)

from django.http import HttpResponse
from .resources.resourse import ArticlesResource  # Подставьте соответствующий путь к вашему ресурсу
from tablib import Dataset

def export_data_to_excel(request):
    dataset = ArticlesResource().export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="your_model_data.xls"'
    return response

#from django.shortcuts import render
#from django.core.cache import cache
#from django.views.decorators.cache import cache_page
#
#@cache_page(60)  # Кэширование результата на 60 секунд
#def news_home(request):
#    news = Articles.objects.order_by('-date')
#    return render(request, 'news/news_home.html', {'news': news})

