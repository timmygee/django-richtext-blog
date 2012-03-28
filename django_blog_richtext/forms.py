from django import forms

from tinymce.widgets import TinyMCE

from models import Post

class PostAdminForm(forms.ModelForm):
    """
    Form for creating and editing posts in the admin section
    """
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 30}))
    
    class Meta:
        model = Post
