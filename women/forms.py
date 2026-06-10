from django import forms
from .models import Women, Category, TagPost

class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label="Теги")

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
        if not all(c in allowed_chars for c in title):
            from django.core.exceptions import ValidationError
            raise ValidationError("Заголовок должен содержать только русские буквы, цифры, дефис и пробел.")
        return title