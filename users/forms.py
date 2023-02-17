from django import forms

from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "example@email.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        email = self.cleaned_data.get("email", None)
        password = self.cleaned_data.get("password", None)
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise forms.ValidationError("Invalid data inputed")
        except models.User.DoesNotExist:
            raise forms.ValidationError("Invalid data inputed")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "phone_number", "skills")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exist", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        phone_number = self.cleaned_data.get("phone_number")
        username = email.split("@")[0]
        user.username = username
        user.phone_number = phone_number
        user.set_unusable_password()
        user.save()
        skills = self.cleaned_data.get("skills")
        if skills:
            for skill in skills.all():
                user.skills.add(skill)
        return user


class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        phone_number = self.cleaned_data.get("phone_number")
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()
        return user
