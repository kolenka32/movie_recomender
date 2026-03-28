from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

User = get_user_model()



from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
            'placeholder': 'Введите ваше имя',
            'autocomplete': 'given-name'
        }),
        error_messages={
            'required': 'Пожалуйста, введите имя'
        }
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
            'placeholder': 'Введите вашу фамилию',
            'autocomplete': 'family-name'
        }),
        error_messages={
            'required': 'Пожалуйста, введите фамилию'
        }
    )

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
            'placeholder': 'Введите имя пользователя',
            'autocomplete': 'username'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
            'placeholder': 'example@mail.com',
            'autocomplete': 'email'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
            'placeholder': 'Создайте пароль',
            'autocomplete': 'new-password'
        })
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем стандартные help_text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if len(password1) < 8:
                raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
            if not any(char.isdigit() for char in password1):
                raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            # Сохраняем пароль отдельно, если нужно дополнительное хеширование
            user.set_password(self.cleaned_data['password1'])
            user.save()

        return user

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
        'placeholder': 'например, alex@netflix.com или alex123',
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'input-premium w-full bg-neutral-900/80 border border-neutral-700 rounded-xl py-3.5 px-4 text-white placeholder:text-neutral-500 focus:border-red-600 transition-all duration-200',
        'placeholder': 'Введите пароль'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive')
        return self.cleaned_data


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')