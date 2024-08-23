from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
 path('',views.index.as_view(), name="income"),
 path('add_income/',views.add_income.as_view(), name="add_income"),
 path('edit_income/<int:id>/',views.edit_income.as_view(), name="edit_income"),
 path('delete_income/<int:id>/',views.delete_income.as_view(), name="delete_income"),
 path('income_source_summary_all/',views.income_source_summary_all,name='income_source_summary_all'),
 path('expense_category_summary_all/',views.expense_category_summary_all,name='expense_category_summary_all')

]