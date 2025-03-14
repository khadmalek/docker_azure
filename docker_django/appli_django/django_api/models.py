from django.db import models
from django.db.models import CASCADE, SET_DEFAULT, SET_NULL
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Create your models here.



class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    sexe = models.CharField(max_length=50, choices=[("homme", "homme"), ("femme", "femme")], null = True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=[("client", "client"), ("conseiller", "conseiller")], default="client")


class LoanRequest(models.Model):
    client = models.ForeignKey(User, on_delete=CASCADE, related_name="loan_requests")  # client de la demande
    conseiller = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name="managed_loans")  # conseiller - peut être nul
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    bank = models.CharField(max_length=100)
    bank_state = models.CharField(max_length=100)
    naics = models.CharField(max_length=10)
    approval_fy = models.CharField(max_length=4)    # année d'approbation
    term = models.PositiveIntegerField()            # durée en mois
    no_emp = models.PositiveIntegerField()          # nombre d'employés
    new_exist = models.CharField(max_length=50)     # nouveau ou existant
    create_job = models.PositiveIntegerField()      # nombre d'emplois créés
    retained_job = models.PositiveIntegerField()    # nombre d'emplois conservés
    franchise_code = models.CharField(max_length=10)
    urban_rural = models.CharField(max_length=50)
    low_doc = models.BooleanField(default=False)    # documentation allégée (oui/non)
    disbursement_gross = models.DecimalField(max_digits=12, decimal_places=2)  # montant du prêt versé
    gr_appv = models.DecimalField(max_digits=12, decimal_places=2)  # montant approuvé
    rev_line_cr = models.BooleanField(default=False)  # ligne de crédit renouvelable (oui/non)
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]
    request_result = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)  # date heure automatiques
    updated_at = updated_at = models.DateTimeField(auto_now=True)


class News(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE, related_name="news")  # conseiller auteur de l'article
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)  # date auto


class Conversation(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=CASCADE, related_name="messages")
    sender = models.ForeignKey(get_user_model(), on_delete=CASCADE, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)



