import django_filters
from django import forms
from .models import Notification

class NotificationFilter(django_filters.FilterSet):

    message = django_filters.CharFilter(
        field_name='message',
        lookup_expr='icontains',
        label='Arama',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Aramak istediğiniz kelimeyi yazın.'
        })
    )

    class Meta:
        model = Notification
        fields = ['message',]
