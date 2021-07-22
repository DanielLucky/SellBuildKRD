from django import forms
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Введите имя"
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields["email"].widget.attrs["placeholder"] = "Введите Email"
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields["password1"].widget.attrs["placeholder"] = "Ведите пароль"
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields["password2"].widget.attrs["placeholder"] = "Повторите пароль"
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        # username = forms.CharField()
        # password1 = forms.CharField(widget=forms.PasswordInput)
        # password2 = forms.CharField(widget=forms.PasswordInput)
        # email = forms.EmailField()
        fields = ['username', 'password1', 'password2', 'email']


class ImageForm(forms.ModelForm):
    class Meta:
        Image = apps.get_model('Sell', 'Image')
        model = Image
        fields = ('imageSell',)

