from django import forms
from datetime import datetime, date
from .models import User, LoanRequest, News
from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="../../.env")



# region login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')


class CreateClientForm(forms.ModelForm) :
    sexe = forms.ChoiceField(required=True, choices=[('male', 'Homme'), ('female', 'Femme')])
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirmer le mot de passe')


    birth_date = forms.DateField(
        required=True,
        label="Date de naissance",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}))

    class Meta:
        model = User    
        fields = ['first_name', 'last_name', 'sexe', 'birth_date', 'email', 'password', 'confirm_password']
        labels = {
            "first_name" : "Prénom", 
            "last_name" : "Nom",
            "email" : "Email", 
        }

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date')

        if birth_date > datetime.now().date():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur")
        age = (date.today() - birth_date).days // 365
        if age < 18:
            raise forms.ValidationError("Vous devez être majeur")
        return cleaned_data

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return confirm_password

    def save(self, commit=True):
        # Hasher le mot de passe
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        # Définir le username comme étant l'email
        user.username = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class RequestForm(forms.ModelForm):
    state = forms.ChoiceField(choices=[
    ('IN', 'Indiana'),
    ('OK', 'Oklahoma'),
    ('FL', 'Florida'),
    ('CT', 'Connecticut'),
    ('NJ', 'New Jersey'),
    ('NC', 'North Carolina'),
    ('IL', 'Illinois'),
    ('RI', 'Rhode Island'),
    ('TX', 'Texas'),
    ('VA', 'Virginia'),
    ('TN', 'Tennessee'),
    ('AR', 'Arkansas'),
    ('MN', 'Minnesota'),
    ('MO', 'Missouri'),
    ('MA', 'Massachusetts'),
    ('CA', 'California'),
    ('SC', 'South Carolina'),
    ('LA', 'Louisiana'),
    ('IA', 'Iowa'),
    ('OH', 'Ohio'),
    ('KY', 'Kentucky'),
    ('MS', 'Mississippi'),
    ('NY', 'New York'),
    ('MD', 'Maryland'),
    ('PA', 'Pennsylvania'),
    ('OR', 'Oregon'),
    ('ME', 'Maine'),
    ('KS', 'Kansas'),
    ('MI', 'Michigan'),
    ('AK', 'Alaska'),
    ('WA', 'Washington'),
    ('CO', 'Colorado'),
    ('MT', 'Montana'),
    ('WY', 'Wyoming'),
    ('UT', 'Utah'),
    ('NH', 'New Hampshire'),
    ('WV', 'West Virginia'),
    ('ID', 'Idaho'),
    ('AZ', 'Arizona'),
    ('NV', 'Nevada'),
    ('WI', 'Wisconsin'),
    ('NM', 'New Mexico'),
    ('GA', 'Georgia'),
    ('ND', 'North Dakota'),
    ('VT', 'Vermont'),
    ('AL', 'Alabama'),
    ('NE', 'Nebraska'),
    ('SD', 'South Dakota'),
    ('HI', 'Hawaii'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia')], label="État")
    bank = os.getenv("BANK_NAME", None)
    bank_state = os.getenv("BANK_STATE", None)
    new_exist = forms.ChoiceField(choices=((0, "Nouvelle"), (1, "Existante")), label="Statut de l'entreprise")
    urban_rural = forms.ChoiceField(choices=((0, "Urbaine"), (1, "Rurale")), label="Zone géographique")
    class Meta:
        model = LoanRequest
        fields = ["city", "zip_code", "state",  "naics", "approval_fy", "term", "no_emp", "new_exist",  "create_job", "retained_job", "franchise_code",  "urban_rural", "low_doc", "gr_appv", "disbursement_gross", "rev_line_cr"]
        labels = {
            "city": "Ville",
            "state": "État",
            "zip_code": "Code postal",
            "naics": "Code NAICS",
            "approval_fy": "Année d'approbation du crédit",
            "term": "Durée du prêt en mois",
            "no_emp": "Nombre d'employés",
            "create_job": "Nombre d'emplois créés",
            "retained_job": "Nombre d'emplois conservés",
            "franchise_code": "Code de franchise de l'entreprise",
            "low_doc": "Documentation du prêt allégée (Oui/Non)",
            "gr_appv": "Montant total du prêt approuvé",
            "disbursement_gross": "Montant du prêt décaissé",
            "rev_line_cr": "Ligne de crédit renouvelable (Oui/Non)"
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.bank = os.getenv("BANK_NAME")
        instance.bank_state = os.getenv("BANK_STATE")

        if commit:
            instance.save()
        return instance


class NewsForm(forms.ModelForm) :
    class Meta:
        model = News
        fields = ["title", "content"]
        labels = {
            "title": "Titre",
            "content": "Contenu"
        }





