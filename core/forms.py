from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Movie, Genre

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit: user.save()
        return user

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {"rating": forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1,6)]),
                   "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your thoughts..."})}

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "year", "director", "cast", "poster", "description", "genres"]
        widgets = {"genres": forms.CheckboxSelectMultiple}
