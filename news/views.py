from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from .filters import NewsFilterSet, OurWorksFilterSet
from .models import News, OurWorks
from .serializers import NewsSerializer, OurWorksSerializer


class CheckPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_staff


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [CheckPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilterSet


class OurWorksViewSet(ModelViewSet):
    queryset = OurWorks.objects.all()
    serializer_class = OurWorksSerializer
    permission_classes = [CheckPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OurWorksFilterSet


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        if 'search' in self.request.GET:
            try:
                return (News.objects.filter(
                    news_title__icontains=self.request.GET['search']) |
                        News.objects.filter(news_description__icontains=self.request.GET['search']) |
                        News.objects.filter(news_content__icontains=self.request.GET['search']))
            except:
                return News.objects.none()
        return News.objects.all()


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/about_news.html'
    context_object_name = 'news'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        News.objects.filter(pk=self.object.pk).update(news_views_count=F('news_views_count') + 1)
        return response


class NewsAddView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/add_news.html'
    fields = ['news_title', 'news_description', 'news_image', 'news_content']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'news/edit_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_image', 'news_content']
    success_url = reverse_lazy('list_news')

    def test_func(self):
        news = News.objects.get(pk=self.kwargs['pk'])
        return self.request.user == news.news_author

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/confirm_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('list_news')

    def get_queryset(self):
        return super().get_queryset().filter(news_author=self.request.user)


class OurWorksListView(ListView):
    model = OurWorks
    template_name = 'our_works/works_list.html'
    context_object_name = 'works'

    def get_queryset(self):
        if 'search' in self.request.GET:
            try:
                return (OurWorks.objects.filter(
                    work_title__icontains=self.request.GET['search']) |
                        OurWorks.objects.filter(work_description__icontains=self.request.GET['search']))
            except:
                return OurWorks.objects.none()
        return OurWorks.objects.all()


class OurWorksDetailView(DetailView):
    model = OurWorks
    template_name = 'our_works/about_work.html'
    context_object_name = 'works'


class OurWorksCreateView(LoginRequiredMixin, CreateView):
    model = OurWorks
    template_name = 'our_works/add_works.html'
    fields = ['work_title', 'work_description', 'work_image', 'workers', 'work_date']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.work_author = self.request.user
        return super().form_valid(form)


class OurWorksUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = OurWorks
    template_name = 'our_works/edit_works.html'
    fields = ['work_title', 'work_description', 'work_image', 'workers', 'work_date']
    success_url = reverse_lazy('list_works')

    def test_func(self):
        work = OurWorks.objects.get(pk=self.kwargs['pk'])
        return self.request.user == work.work_author

    def form_valid(self, form):
        form.instance.work_author = self.request.user
        return super().form_valid(form)


class OurWorksDeleteView(LoginRequiredMixin, DeleteView):
    model = OurWorks
    template_name = 'our_works/confirm_delete.html'
    context_object_name = 'works'
    success_url = reverse_lazy('list_works')

    def get_queryset(self):
        return super().get_queryset().filter(work_author=self.request.user)
