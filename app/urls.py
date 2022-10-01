from django.urls import path
from .views import *
urlpatterns = [
    path('', homeView, name='home'),
    path('save/', saveView, name = 'save'),
    path('saveincome/', saveIncomeView, name = 'save'),
    path('incomeclient/', incomeView, name = 'incomeclient'),
    path('client/<int:slug>/', clientPageView, name='clientPageView'),
    path('clientpayment/', clientPaymentView, name='ClientPayment'),
    path('incomedehqons/', incomeDehqonView, name='incomedehqon'),
    path('pricechange/', priceChangeView, name='Clientpricechange'),
    path('dehqon/<int:slug>/', dehqonView, name='dehqonpage'),
    path('dehqonincome/', dehqonIncomeView, name='dehqonincome'),
    path('completdehqon/', dehqonCompleteView, name='dehqoncomplete'),
    path('teri/', teriView, name='teri'),
    path('kallahasb/', kallaHasbView, name='kallahasb'),
    path('kirim/', kirimView, name='kirim'),
    path('chiqim/', chiqimView, name='chiqim'),
    path('bron/', bronView, name='bronproduct'),
    path('mijozchange/', mijozchangeView, name='mijozchange'),
    path('login/', loginView, name='login'),
    path('adminkirim/', adminkirimView, name='adminkirim'),
    path('adminchiqim/', adminchiqimView, name='adminchiqim'),
    path('adduser/', adduserView, name='adduser'),
    path('qarz/', qarzView, name='qarz'),
    path('boshqa/', otherexpenseView, name='otherqarz'),
    path('bozorchiqim/', bozorchiqimView, name = 'bozorchiqim'),
    path('bozorboshqachiqim/', bozorboshqachiqimView, name = 'bozorboshqachiqim'),
    path('sotuvchi/<int:slug>/', sotuvchiView, name = 'sotuvchi'),
    path('qushxonastatistic/', qushxonastatisticsView, name = 'qushxonastatistik'),
    path('bozorstatistic/', bozorstatisticsView, name = 'bozorstatistik'),
    path('bozorqarz/', bozorqarzView, name='bozorallqarz'),
    path('searchbox/', SearchboxView, name='searchbox'),
    path('logout/', logoutView, name='logout'),
]