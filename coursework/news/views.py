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

