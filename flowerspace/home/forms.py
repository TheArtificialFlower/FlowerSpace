from django import forms
from django.core.exceptions import ValidationError
from .models import Posts, Hashtag, Comment
import re


class CreatePostForm(forms.ModelForm):
    hashtags = forms.CharField(required=False, widget=forms.TextInput(attrs={"type":"text",
    "id": "hashtagInput", "placeholder": "Type your tag with # and press space...","class": "hashtag-field"}))

    allow_comments = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"type":"checkbox",
    "name":"allow_comments", "onchange":"this.parentElement.classList.toggle('checked', this.checked)"}))

    class Meta:
        model = Posts
        exclude = ("user",)
        fields = "__all__"
        widgets = {
            'image': forms.FileInput(attrs={'id': 'postImage', 'accept': 'image/*', 'class': 'hidden'}),
            'desc': forms.Textarea(attrs={"class": "form-textarea", "placeholder":"Write your floral story...","rows":"4"}),
        }

    def clean_hashtags(self):
        hashtag_str = self.cleaned_data.get("hashtags", "")
        hashtags = list(set(re.findall(r"#\w+", hashtag_str)))
        if len(hashtags) > 10:
            raise ValidationError("Hashtags cannot be more than 10.")
        return hashtags



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            'text': forms.TextInput(attrs={'rows':2, 'placeholder':'Add a comment....', 'class':'textarea'})
        }

