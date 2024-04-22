import django_filters
from .models import Members, Organizations


class MembersFilter(django_filters.FilterSet):
    class Meta:
        model = Members
        fields = ['id', 'memeber_name', 'member_president', 'memmber_added_date']


class OrganizationsFilter(django_filters.FilterSet):
    class Meta:
        model = Organizations
        fields = ['id', 'organization_name', 'organization_president', 'organization_organizate_date']
