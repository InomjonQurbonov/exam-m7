from django.urls import path, include
from rest_framework import routers

from .views import (
    MembersViewSet, OrganizationsViewSet, MemberListView,
    MemberDetailView, MemberCreateView, MemberUpdateView, MemberDeleteView,
    OrganizationListView, OrganizationDetailView, OrganizationCreateView,
    OrganizationUpdateView, OrganizationDeleteView
)

router = routers.DefaultRouter()
router.register(r'members', MembersViewSet)
router.register(r'organizations', OrganizationsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # members
    path('members/', MemberListView.as_view(), name='members-list'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='members-detail'),
    path('members/create/', MemberCreateView.as_view(), name='members-create'),
    path('members/<int:pk>/update/', MemberUpdateView.as_view(), name='members-update'),
    path('members/<int:pk>/delete/', MemberDeleteView.as_view(), name='members-delete'),
    # organizations
    path('organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organizations-detail'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organizations-create'),
    path('organizations/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organizations-update'),
    path('organizations/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organizations-delete'),
]
