from django.urls import path
from . import views



urlpatterns = [
   path("", views.index, name="index"),
   path("<int:month>", views.monthly_challenge_by_number),
   path("<str:month>", views.monthly_challenge, name="month_challenge"),
   path('save-meanings/', views.save_lenormand_card_meanings, name='save_lenormand_card_meanings'),
   path('save-combinations/', views.save_lenormand_combinations, name='save_lenormand_cards_combinations'),
   path('save-lenormand-keywords/', views.save_lenormand_keywords, name='save_lenormand_keywords')
]
