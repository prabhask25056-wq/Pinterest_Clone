from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PinForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()

    def clean_image(self):
        img = self.cleaned_data['image']
        if img.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image must be under 5 MB.")
        return img