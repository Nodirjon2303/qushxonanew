from django.urls import path
from .views import *

urlpatterns = [
    path('', homeView, name='home'),
    path('save/', saveView, name='save'),
    path('saveincome/', saveIncomeView, name='save'),
    path('incomeclient/', incomeView, name='incomeclient'),
    path('bozor-bozor-income/', BozorBozorIncomeView.as_view(), name='bozor-bozor-kirim'),
    path('bozor-bozor-income/<int:pk>/update/', BozorBozorIncomeUpdateView.as_view(), name='bozor-bozor-kirim-update'),
    path('bazar-bazar-add/', BazarBazarCreateView.as_view(), name='bazar-bazar-add'),
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
    path('adminkirim/', AdminQushxonaKirimListView.as_view(), name='adminkirim'),
    path('admin-bozor-kirim/', AdminBozorKirimListView.as_view(), name='admin-bozor-kirim'),
    path('adminkirim-excel/', AdminQushxonaKirimExcelView.as_view(), name='adminkirim-excel'),
    path('admin-bozor-kirim-excel/', AdminBozorKirimExcelView.as_view(), name='admin-bozor-kirim-excel'),
    path('adminchiqim-excel/', AdminQushxonaChiqimExcelView.as_view(), name='adminchiqim-excel'),
    path('admin-bozor-chiqim-excel/', AdminBozorChiqimExcelView.as_view(), name='admin-bozor-chiqim-excel'),
    path('adminchiqim/', AdminChiqimListView.as_view(), name='adminchiqim'),
    path('admin-bozor-chiqim/', AdminBozorChiqimListView.as_view(), name='admin-bozor-chiqim'),
    path('adduser/', adduserView, name='adduser'),
    path('qarz/', qarzView, name='qarz'),
    path('boshqa/', otherexpenseView, name='otherqarz'),
    path('bozorchiqim/', bozorchiqimView, name='bozorchiqim'),
    path('bozor-chiqim-create/', BazarChiqimCreateView.as_view(), name='bazar-chiqim-create'),
    path('bozorboshqachiqim/', bozorboshqachiqimView, name='bozorboshqachiqim'),
    path('sotuvchi/<int:slug>/', sotuvchiView, name='sotuvchi'),
    path('sotuvchi/add-payment/<int:pk>/', SotuvchiCreateView.as_view(), name='sotuvchi-add-payment'),
    # path('sotuvchi/<int:pk>/update/', SotuvchiUpdatePaymentView.as_view(), name='sotuvchi-update'),
    path('sotuvchi/payments/savdo/<int:pk>/', SotuvchiSavdoListPaymentsView.as_view(), name='sotuvchi-savdo-list'),
    path('qushxonastatistic/', qushxonastatisticsView, name='qushxonastatistik'),
    path('bozorstatistic/', bozorstatisticsView, name='bozorstatistik'),
    path('bozorqarz/', bozorqarzView, name='bozorallqarz'),
    path('searchbox/', SearchboxView, name='searchbox'),
    path('logout/', logoutView, name='logout'),
]
