from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, ListView, FormView
from .forms import LoginForm, CreateClientForm, RequestForm, NewsForm
from .models import User, LoanRequest, News
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.db.models import Q
from django.http import JsonResponse
from .api_utils import loan_request_to_api
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="../../.env")
BANK_NAME = os.getenv("BANK_NAME")
BANK_STATE = os.getenv("BANK_STATE")


# Create your views here.



# region -home page
class HomePageView(View):       # OK +-
    template_name = "home_page.html"

    def get(self, request):
        return render(request, self.template_name)


# region -authentication
class AuthenticationView(View) :    # OK +-
    template_name = "authentication.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("profil")
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"],)
            if user is not None:
                login(request, user)
                return redirect("profil")
            else:
                message = "Identifiants invalides."
        return render(request, self.template_name, {"form": form, "message": message})


# region -Deconnexion
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('home')


# region -create profil
class CreateClientView(View) :      # OK+-
    model = User
    form_class = CreateClientForm
    template_name = 'create_client.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            form.save()
            messages.success(request, "Compte créé avec succès!")
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


# region -profil view
class ProfilView(View) :            # OK+
    template_name = 'profil.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})

# region -bank news
class BankNewsView(View):
    template_name = 'news.html'

    def get(self, request):
        news_list = News.objects.all().order_by('-publication_date')
        return render(request, self.template_name, {'news_list': news_list})

    def post(self, request):
        if request.POST.get('action') == 'delete':
            news_id = request.POST.get('news_id')
            if news_id:
                news = News.objects.get(id=news_id)
                # Vérifier que seul l'auteur ou un superuser peut supprimer
                if request.user == news.author or request.user.is_superuser:
                    news.delete()
                    messages.success(request, 'Article supprimé avec succès')
                else:
                    messages.error(request, 'Vous n\'avez pas la permission de supprimer cet article')
        return redirect('news')


class AddNewsView(LoginRequiredMixin, View):        # LoginRequiredMixin remplace if not request.user.is_authenticated
    template_name = 'create_news.html'
    form_class = NewsForm

    def test_func(self):
        return self.request.user.user_type == "conseiller" or self.request.user.is_superuser

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Article ajouté avec succès')
            return redirect('news')
        return render(request, self.template_name, {'form': form})


# region -loan request
class LoanRequestView(View):
    model = LoanRequest
    form_class = RequestForm
    template_name = 'loan_request.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.client = request.user

            # Préparer les données pour l'API dans le format attendu
            donnees = {
                "ApprovalFY": int(loan_request.approval_fy),
                "Bank": BANK_NAME,
                "BankState": BANK_STATE,
                "City": loan_request.city.upper(),
                "CreateJob": loan_request.create_job,
                "DisbursementGross": float(loan_request.disbursement_gross),
                "FranchiseCode": int(loan_request.franchise_code),
                "GrAppv": float(loan_request.gr_appv),
                "LowDoc": 1 if loan_request.low_doc else 0,
                "NAICS": int(loan_request.naics),
                "NewExist": int(loan_request.new_exist),
                "NoEmp": loan_request.no_emp,
                "RetainedJob": loan_request.retained_job,
                "RevLineCr": 1 if loan_request.rev_line_cr else 0,
                "State": loan_request.state,
                "Term": loan_request.term,
                "UrbanRural": int(loan_request.urban_rural),
                "Zip": int(loan_request.zip_code.replace("-", ""))
            }

            try:
                # Appeler l'API
                api_result = loan_request_to_api(donnees)

                # Mettre à jour le résultat dans la base de données
                loan_request.request_result = "accepted" if api_result else "refused"
                loan_request.save()

                return render(request, 'loan_result.html', {
                    'result': api_result,
                    'loan_request': loan_request,
                    'success': True
                })

            except Exception as e:
                messages.error(request, f"Une erreur s'est produite lors de l'analyse: {str(e)}")
                return render(request, 'loan_result.html', {
                    'error': str(e),
                    'loan_request': loan_request,
                    'success': False
                })

        return render(request, self.template_name, {'form': form})


class LoanRequestsListView(View) :
    template_name = 'loan_request_list.html'

    def get(self, request) :
        if not request.user.is_authenticated:
            messages.error(request, "Veuillez vous connecter pour accéder à cette page")
            
        # if request.user.is_authenticated :
        if request.user.user_type == "conseiller" :
            loan_requests = LoanRequest.objects.all().order_by("request_date")
        else : 
            loan_requests = LoanRequest.objects.filter(client = request.user).order_by("request_date")
            
        context = {
            'loan_requests': loan_requests,
            'is_conseiller': request.user.user_type == "conseiller"
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Non autorisé'}, status=401)

        if request.user.user_type == "conseiller":
            # Récupération des paramètres
            action = request.POST.get('action')
            loan_id = request.POST.get('loan_id')

            if action and loan_id:
                try:
                    loan_request = LoanRequest.objects.get(id=loan_id)

                    if action == 'delete':
                        loan_request.delete()
                        messages.success(request, "Demande supprimée avec succès")
                        return redirect('loan_requests_list')

                    elif action == 'update_status':
                        new_status = request.POST.get('status')
                        if new_status in ['approved', 'rejected']:
                            loan_request.request_result = new_status
                            loan_request.save()
                            messages.success(request, f"Statut mis à jour : {new_status}")
                        else:
                            messages.error(request, "Statut invalide")
                        return redirect('loan_requests_list')

                except LoanRequest.DoesNotExist:
                    messages.error(request, "Demande de prêt non trouvée")
                    return redirect('loan_requests_list')

            # Gestion de la recherche
            last_name = request.POST.get("last_name", "").strip()
            first_name = request.POST.get("first_name", "").strip()

            if last_name or first_name:
                from django.db.models import Q
                query = Q()
                if last_name:
                    query |= Q(client__last_name__icontains=last_name)
                if first_name:
                    query |= Q(client__first_name__icontains=first_name)

                loan_requests = LoanRequest.objects.filter(query).order_by('request_date')

                context = {
                    'loan_requests': loan_requests,
                    'is_conseiller': True,
                    'selected_last_name': last_name,
                    'selected_first_name': first_name
                }
                return render(request, self.template_name, context)

        return redirect('loan_requests_list')


# region -chat
class ChatView(View) :
    pass


# region -BONUS
# class PasswordResetView(View) :         # bonus
#     pass
