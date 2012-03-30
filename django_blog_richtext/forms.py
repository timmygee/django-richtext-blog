from django import forms
from django.contrib.auth.models import User

from tinymce.widgets import TinyMCE

from models import Post

class PostFormAdmin(forms.ModelForm):
    """
    Form for creating and editing posts in the admin section
    """
    content = forms.CharField(required=False,
        widget=TinyMCE(attrs={'cols': 100, 'rows': 30}))

    class Meta:
        model = Post

