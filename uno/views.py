from django.views.generic import ListView

from news.models import News, OurWorks


class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'items'

    def get_queryset(self):
        news_queryset = News.objects.all()
        works_queryset = OurWorks.objects.all()
        return list(news_queryset) + list(works_queryset)
