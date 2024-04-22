from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from .filters import MembersFilter, OrganizationsFilter
from .models import Members, Organizations
from .serializers import MembersSerializer, OrganizationsSerializer


class CheckPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_staff


class MembersViewSet(ModelViewSet):
    queryset = Members.objects.all()
    serializer_class = MembersSerializer
    permission_classes = [CheckPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MembersFilter


class OrganizationsViewSet(ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationsSerializer
    permission_classes = [CheckPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrganizationsFilter


class MemberListView(ListView):
    model = Members
    template_name = 'members/members_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        if 'search' in self.request.GET:
            try:
                return (Members.objects.filter(
                    memeber_name__icontains=self.request.GET['search']))
            except:
                return Members.objects.none()
        return Members.objects.all()


class MemberDetailView(DetailView):
    model = Members
    template_name = 'members/about_member.html'
    context_object_name = 'member'


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Members
    template_name = 'members/add_members.html'
    fields = ['memeber_name', 'memmber_added_date', 'member_president', 'member_image']
    success_url = reverse_lazy('members_list')

    def form_valid(self, form):
        form.instance.member_author = self.request.user
        return super().form_valid(form)


class MemberUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Members
    template_name = 'members/edit_members.html'
    fields = ['memeber_name', 'memmber_added_date', 'member_president', 'member_image']
    success_url = reverse_lazy('members-list')

    def test_func(self):
        news = Members.objects.get(pk=self.kwargs['pk'])
        return self.request.user == news.member_author

    def form_valid(self, form):
        form.instance.member_author = self.request.user
        return super().form_valid(form)


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Members
    template_name = 'members/confirm_delete.html'
    context_object_name = 'member'
    success_url = reverse_lazy('members_list')

    def get_queryset(self):
        return super().get_queryset().filter(member_author=self.request.user)


class OrganizationListView(ListView):
    model = Organizations
    template_name = 'organizations/organizations_list.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        if 'search' in self.request.GET:
            try:
                return (Organizations.objects.filter(
                    organization_name__icontains=self.request.GET['search']))
            except:
                return Organizations.objects.none()
        return Organizations.objects.all()


class OrganizationDetailView(DetailView):
    model = Organizations
    template_name = 'organizations/about_organizations.html'
    context_object_name = 'organization'


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organizations
    template_name = 'organizations/add_organizations.html'
    fields = ['organization_name', 'organization_organizate_date', 'organization_logo', 'organization_president',
              'organization_link']
    success_url = reverse_lazy('organizations-list')

    def form_valid(self, form):
        form.instance.organization_author = self.request.user
        return super().form_valid(form)


class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organizations
    template_name = 'organizations/edit_organizations.html'
    fields = ['organization_name', 'organization_organizate_date', 'organization_logo', 'organization_president',
              'organization_link']
    success_url = reverse_lazy('organizations-list')

    def test_func(self):
        news = Organizations.objects.get(pk=self.kwargs['pk'])
        return self.request.user == news.organization_author

    def form_valid(self, form):
        form.instance.organization_author = self.request.user
        return super().form_valid(form)


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organizations
    template_name = 'organizations/confirm_delete.html'
    context_object_name = 'organization'

    def get_queryset(self):
        return super().get_queryset().filter(organization_author=self.request.user)
