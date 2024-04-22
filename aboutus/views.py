from django.views.generic import ListView

from members.models import Members, Organizations


class AboutUs(ListView):
    template_name = 'aboutus/aboutus.html'
    context_object_name = 'items'

    def get_queryset(self):
        members_queryset = Members.objects.all()
        organizations_queryset = Organizations.objects.all()
        return list(members_queryset) + list(organizations_queryset)
