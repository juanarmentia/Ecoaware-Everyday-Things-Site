from django.forms import ModelForm, CharField, PasswordInput, RegexField, ValidationError, EmailField, Form, ChoiceField, RadioSelect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Device, User_Question, CustomUser, TagRFID


class UserCreateForm(ModelForm):
    username = RegexField(label="Username", max_length=30, regex=r'^\w+$',error_message ="This value must contain only letters, numbers and underscores. Required 30 characters or fewer.")
    email = EmailField(label="E-mail", max_length=75)
    password1 = CharField(label="Password", widget=PasswordInput) 
    password2 = CharField(label="Password confirmation", widget=PasswordInput) 
    
    class Meta: 
        model = User 
        fields = ('username', 'email',) 
    
    def clean_username(self): 
        username = self.cleaned_data["username"] 
        try: 
            User.objects.get(username=username) 
        except User.DoesNotExist: 
            return username 
        raise ValidationError("A user with that username already exists.")
    
    def clean_email(self): 
        email = self.cleaned_data["email"] 
        try: 
            User.objects.get(email=email) 
        except User.DoesNotExist: 
            return email 
        raise ValidationError("A user with that email already exists.")
    
    def clean_password2(self): 
        password1 = self.cleaned_data.get("password1") 
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2: 
            raise ValidationError("The two password fields didn't match.")
        return password2 
    
    def save(self, commit=True): 
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"]) 
        if commit: 
            user.save() 
        return user 


class UserUpdateForm(ModelForm):
    email = EmailField(label="E-mail", max_length=75) 
    
    class Meta: 
        model = User 
        fields = ('email',) 


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('rfid', 'twitter')
    
    def __init__(self, *args, **kwargs):
       super(CustomUserForm, self).__init__(*args, **kwargs)
       instance = getattr(self, 'instance', None)
       if instance: 
          self.fields['rfid'].widget.attrs['readonly'] = True
        
    def clean_twitter(self): 
        twitter = self.cleaned_data["twitter"] 
        try: 
            CustomUser.objects.get(twitter=twitter) 
        except CustomUser.DoesNotExist: 
            return twitter 
        raise ValidationError("Ya existe un usuario con esta cuenta de Twitter.")
    
    
class CustomUserUpdateForm(ModelForm):
    twitter = CharField(max_length=15, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('twitter',)
        


class DevicesForm(ModelForm):
    class Meta:
        model = Device
 
    
class RfidForm(ModelForm):
    class Meta:
        model = TagRFID
        exclude = ['active', 'device']
        


CHOICES=((1, 'answer_1'), (2, 'answer_2'), (3, 'answer_3'))

 
class User_QuestionForm(ModelForm):
    class Meta:
        model = User_Question   
    
    
    
    
    
    
