from django.urls import path
from app.views import *
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='home'),
    path('utilisateurs/', utilisateurs, name="pageutilisateur"),
    path('requettes/', requettes, name="pagerequettes"),
    path('login_register/', login, name="login"),
    path('update/<int:id>/', update, name="update"),
    path('delete/<int:id>/', delete, name="delete"),
    path('register/', register, name="register"),
    path('connexion/', connexion, name="connexion"),
    path('transactionuserid/<int:id>/', transactionuserid, name="transactionuserid"),
    path('detailrequette/<int:id>/', detailrequette, name="detailrequette"),
    path('requettes/detailrequette/<int:id>/', detailrequetteacc, name="detailrequette"),
    path('requetteuserid/<int:id>/', requetteuserid, name="requetteuserid"),
    path('updatetransaction/<int:id>/', updatetransaction, name="updatetransaction"),
    path('userconnexion', pageuser, name="pageuser"),
    path('deconnexion', deconnexion, name="deconnexion"),
    path('initrequettes/<int:id>/', envoilarequette, name="envoilarequette"),
    path('api_viewutilisateurs', api_view, name="api_view"),
    path('detailutilisateur/<int:pk>/', detailUtilisateurView.as_view(), name="detailUtilisateurView"),
    path('creatreutilisateur/', CreateUtilisateurView.as_view(), name="CreateUtilisateurView"),
    path('updateutilisateur/<int:pk>/', UpdateUtilisateurView.as_view(), name="UpdateUtilisateurView"),
    path('updatesoldeutilisateur/<int:pk>/', UpdateSoldeUtilisateurView.as_view(), name="UpdateSoldeUtilisateurView"),
    path('updatecompteutilisateur/<int:pk>/', UpdateUtilisateurCompteView.as_view(), name="UpdateUtilisateurCompteView"),
    path('deleteutilisateur/<int:pk>/', DeleteUtilisateurView.as_view(), name="DeleteUtilisateurView"),
    path('listeutilisateur/', ListeUtilisateurView.as_view(), name="ListeUtilisateurView"),
] 