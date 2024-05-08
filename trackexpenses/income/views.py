from django.shortcuts import render,redirect
from .models import Source,Income
from expenseapp.models import Category,Expense
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import datetime
from django.http import JsonResponse


@login_required(login_url='/authentication/login')
def index(request):
 source=  Source.objects.all()
 income=Income.objects.filter(owner=request.user) 
 paginator=Paginator(income,3) 
 page_number=request.GET.get('page' ) 
 page_obj=paginator.get_page(page_number) 
 totalpage=page_obj.paginator.num_pages; 
 context={
  'income':income,
  'page_obj':page_obj,
  'totalpageList': [n+1 for n in range(totalpage)],
  'totalpage':totalpage
 }
 return render(request,'income/index.html',context)


@login_required(login_url='/authentication/login')
def add_income(request):

 sources= Source.objects.all()
 context={
  'sources':sources,
  'values':request.POST
 }
 if request.method=='GET':
   return render(request,'income/add_income.html',context)

 if request.method=='POST':
  amount=request.POST['amount']
  description=request.POST['description']  
  date=request.POST['dateOfIncome'] 
  source=request.POST['source'].upper()

  if not amount :
   messages.error(request,"Amount is required")
   return render(request,'income/add_income.html',context)
  

  if not description :
    messages.error(request,"Description is required")
    return render(request,'income/add_income.html',context)
  
  if not date :
    messages.error(request,"All the fields are required")
    return render(request,'income/add_income.html',context)
  
  if not source :
    messages.error(request,"All the fields are required")
    return render(request,'income/add_income.html',context)
  try:
            # Check for existing source (case-insensitive)
            source = Source.objects.get(name__iexact=source)
  except Source.DoesNotExist:
            # Create new source if it doesn't exist
            source = Source.objects.create(name=source)


  Income.objects.create(owner=request.user,amount=amount,date=date,source=source,description=description) 
  expenses=Income.objects.filter(owner=request.user)
  context={
  'source':source
  }
  messages.success(request,'Income saved succesfully!!')
  return redirect('income')


@login_required(login_url='/authentication/login')
def edit_income(request,id):
 income=Income.objects.get(pk=id)
 sources= Source.objects.all()
 context={
  'income':income,
  'values':income,
  'sources':sources
  
 }

 if request.method=='GET':
  return render(request,'income/edit_income.html',context)
 if request.method=='POST':
  amount=request.POST['amount']
  description=request.POST['description']  
  date=request.POST['dateOfIncome'] 
  source=request.POST['source'].upper()

  if not amount :
   messages.error(request,"Amount is required")
   return render(request,'income/edit_expense.html',context)
  

  if not description :
    messages.error(request,"Description is required")
    return render(request,'income/edit_expense.html',context)
  
  if not date :
    messages.error(request,"Description is required")
    return render(request,'income/edit_expense.html',context)
  
  if not source :
    messages.error(request,"Description is required")
    return render(request,'income/edit_expense.html',context)
  try:
         
            source = Source.objects.get(name__iexact=source)
  except Source.DoesNotExist:
            
            source = Source.objects.create(name=source)
  
  


  income.owner=request.user
  income.amount= amount
  income.date= date
  income.source=source.name
  income.description=description
  income.save()
  messages.success(request,'Expense updated successfully')

  return redirect('income')
 
def delete_income(request,id):
  income=Income.objects.get(pk=id)  
  income.delete()
  messages.success(request,'Income record removed')
  return redirect('income')




from django.http import JsonResponse

def income_source_summary_all(request):
    income = Income.objects.filter(owner=request.user)
    finalrep = {}

    def get_income_source_amount(source):
        filtered_by_source = income.filter(source=source)
        amount = sum(item.amount for item in filtered_by_source)
        return amount

    source_list = set(income.values_list('source', flat=True))

    for source in source_list:
        finalrep[source] = get_income_source_amount(source)

    total_sum = sum(finalrep.values())

    combined = {
        'income_category_data_all': finalrep,
        'total_sum': total_sum
    }

    return JsonResponse(combined, safe=False)


def expense_category_summary_all(request):
    expense = Expense.objects.filter(owner=request.user)
    finalrep = {}

    def get_expense_category_amount(category):
        filtered_by_category = expense.filter(category=category)
        amount = sum(item.amount for item in filtered_by_category)
        return amount

    category_list = set(expense.values_list('category', flat=True))

    for category in category_list:
        finalrep[category] = get_expense_category_amount(category)

    total_sum = sum(finalrep.values())

    combined = {
        'expense_category_data_all': finalrep,
        'total_sum': total_sum
    }

    return JsonResponse(combined, safe=False)



