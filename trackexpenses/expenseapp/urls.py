from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
 path('',views.index.as_view(), name="expenses"),
 path('add_expense/',views.add_expense.as_view(), name="add_expense"),
 path('edit_expense/<int:id>/',views.edit_expense.as_view(), name="edit_expense"),
 path('delete_expense/<int:id>/',views.delete_expense.as_view(), name="delete_expense"),
 # path('add',views.add_expense, name="add-expenses")
 path('search_expenses',csrf_exempt(views.search_expenses), name="search_expenses"),
 path('expense_category_summary',views.expense_category_summary,name='expense_category_summary'),
 path('income_source_summary',views.income_source_summary,name='income_source_summary'),
 path('stats',views.stats,name='stats')
]
