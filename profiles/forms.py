from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = UserProfile
        fields = ['username', 'profile_image', 'gender', 'custom_gender']
        widgets = {
            'gender': forms.Select(choices=UserProfile.GENDER_CHOICES, attrs={'class': 'form-select'}),
        }
        labels = {
            'profile_image': 'Profile Image',
            'custom_gender': 'If other, please specify',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'username',
            'profile_image',
            'gender',
            'custom_gender',
            Submit('submit', 'Save changes', css_class='btn btn-primary')
        )
        # Prepopulate the user fields
        if 'instance' in kwargs:
            user = kwargs['instance'].user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False)
    custom_gender = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Make email field mandatory

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        gender = self.cleaned_data.get('gender')
        custom_gender = self.cleaned_data.get('custom_gender')

        UserProfile.objects.create(
            user=user,
            username=user.username,
            gender=gender,
            custom_gender=custom_gender,
        )

        return user