import django_filters

from news.models import News, OurWorks


class NewsFilterSet(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains', field_name='news_title', name='news_title')

    class Meta:
        model = News
        fields = ['id', 'news_title', 'news_date', 'news_views_count', ]


class OurWorksFilterSet(django_filters.FilterSet):
    class Meta:
        model = OurWorks
        fields = ['id', 'work_title', 'work_date']
