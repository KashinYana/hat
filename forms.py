# -*- coding: utf-8 -*-

from django import forms

class WordForm(forms.Form):
    word1 = forms.CharField(label='1', required=False)    
    word2 = forms.CharField(label='2', required=False)    
    word3 = forms.CharField(label='3', required=False)    
    word4 = forms.CharField(label='4', required=False)    
    word5 = forms.CharField(label='5', required=False)    
    word6 = forms.CharField(label='6', required=False)    
    word7 = forms.CharField(label='7', required=False)    
    word8 = forms.CharField(label='8', required=False)    
    word9 = forms.CharField(label='9', required=False)    
    word10 = forms.CharField(label='10', required=False)  
        
class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин')
    email = forms.CharField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

class UserProfileForm(forms.Form):
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput,
        help_text="Заполните, чтобы поменять пароль, или оставьте поле пустым", required=False)
    new_password_repeated = forms.CharField(label='Новый пароль ещё раз', widget=forms.PasswordInput, required=False)
