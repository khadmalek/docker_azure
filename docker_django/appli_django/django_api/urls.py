from django.urls import path
from .views import HomePageView, AuthenticationView, CreateClientView, ProfilView, LoanRequestView, BankNewsView, AddNewsView, logout_view, LoanRequestsListView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  
    path('authentication/', AuthenticationView.as_view(), name='authentication'),  
    path('create_client/', CreateClientView.as_view(), name='create_client'),  
    path('profil/', ProfilView.as_view(), name='profil'),  
    path('loan_request/', LoanRequestView.as_view(), name='loan_request'),
    path('news/', BankNewsView.as_view(), name='news'),
    path('add_news/', AddNewsView.as_view(), name='add_news'),
    path('logout/', logout_view, name='logout'),
    path('loan_requests_list/', LoanRequestsListView.as_view(), name='loan_requests_list'),
    
    path('article1/', TemplateView.as_view(template_name='article1.html'), name='article1'),
    path('article2/', TemplateView.as_view(template_name='article2.html'), name='article2'),
    path('article3/', TemplateView.as_view(template_name='article3.html'), name='article3')   
        ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)