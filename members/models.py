from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Members(models.Model):
    memeber_name = models.CharField(max_length=255)
    memmber_added_date = models.DateTimeField()
    member_president = models.CharField(max_length=255)
    member_image = models.ImageField(upload_to='member/', default='members/uno.png', blank=True)
    member_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.memeber_name

    class Meta:
        ordering = ['id', ]
        db_table = 'members'
        verbose_name = "Members"


class Organizations(models.Model):
    organization_name = models.CharField(max_length=255)
    organization_organizate_date = models.DateTimeField()
    organization_president = models.CharField(max_length=255)
    organization_logo = models.ImageField(upload_to='organization/', blank=True)
    organization_link = models.URLField(blank=True)
    organization_author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.organization_name

    class Meta:
        ordering = ['id', ]
        db_table = 'organizations'
        verbose_name = "Organizations"
