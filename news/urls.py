from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet, OurWorksViewSet, NewsListView,
    NewsDetailView, NewsAddView, UpdateNewsView,
    DeleteNewsView, OurWorksListView, OurWorksDetailView,
    OurWorksCreateView, OurWorksUpdateView, OurWorksDeleteView
)

router = DefaultRouter()

router.register(r'news/api', NewsViewSet)
router.register(r'ourworks/api', OurWorksViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('news/', NewsListView.as_view(), name='list_news'),
    path('news/detail/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('add_news/', NewsAddView.as_view(), name='add_news'),
    path('news/update/<int:pk>/', UpdateNewsView.as_view(), name='update_news'),
    path('news/delete/<int:pk>/', DeleteNewsView.as_view(), name='delete_news'),
    # our_works
    path('works/', OurWorksListView.as_view(), name='list_works'),
    path('works/<int:pk>/', OurWorksDetailView.as_view(), name='works_detail'),
    path('works/add/', OurWorksCreateView.as_view(), name='add_work'),
    path('works/update/<int:pk>/', OurWorksUpdateView.as_view(), name='update_work'),
    path('works/delete/<int:pk>/', OurWorksDeleteView.as_view(), name='delete_work'),
]
