from django.urls import path
from .views import ExchangeRateView,home,all_subscriptions_view, dashboard_view,SubscribeView, SubscriptionListView, CancelSubscriptionView


urlpatterns = [
    path('api/subscribe/', SubscribeView.as_view()),
    path('api/subscriptions/', SubscriptionListView.as_view()),
    path('api/cancel/', CancelSubscriptionView.as_view()),
    # path('api/exchange-rate/', ExchangeRateView.as_view()),
    path('subscriptions/', all_subscriptions_view),
    path('', home, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # path('test-insert/', test_insert_exchange_rates),
    path('api/exchange-rate/', ExchangeRateView.as_view()),
    

]
