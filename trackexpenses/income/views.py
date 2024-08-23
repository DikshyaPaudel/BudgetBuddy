from django.shortcuts import render,redirect
from .models import Source,Income
from expenseapp.models import Category,Expense
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

import datetime

from rest_framework.permissions import IsAuthenticated
from .serializers import IncomeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


# @login_required(login_url='/authentication/login')
# def index(request):
#  source=  Source.objects.all()
#  income=Income.objects.filter(owner=request.user) 
#  paginator=Paginator(income,3) 
#  page_number=request.GET.get('page' ) 
#  page_obj=paginator.get_page(page_number) 
#  totalpage=page_obj.paginator.num_pages; 
#  context={
#   'income':income,
#   'page_obj':page_obj,
#   'totalpageList': [n+1 for n in range(totalpage)],
#   'totalpage':totalpage
#  }
#  return render(request,'income/index.html',context)

class index(APIView):
    def get(self, request):
        income = Income.objects.filter(owner=request.user)
        
        serializer = IncomeSerializer(income, many=True)
        return Response(serializer.data)
        


# @login_required(login_url='/authentication/login')
# def add_income(request):
#  sources = [
#     ("Salary", "Salary"),
#     ("Side Job", "Side Job"),
#     ("Business", "Business"),
#   ]

# #  sources= Source.objects.all()

#  context={
#   'sources':sources,
#   'values':request.POST
#  }
#  if request.method=='GET':
#    return render(request,'income/add_income.html',context)

#  if request.method=='POST':
#   amount=request.POST['amount']
#   description=request.POST['description']  
#   date=request.POST['dateOfIncome'] 
#   source=request.POST['source']

#   if not amount :
#    messages.error(request,"Amount is required")
#    return render(request,'income/add_income.html',context)
  

#   if not description :
#     messages.error(request,"Description is required")
#     return render(request,'income/add_income.html',context)
  
#   if not date :
#     messages.error(request,"All the fields are required")
#     return render(request,'income/add_income.html',context)
  
#   if not source :
#     messages.error(request,"All the fields are required")
#     return render(request,'income/add_income.html',context)
#   # try:
#   #           # Check for existing source (case-insensitive)
#   #           source = Source.objects.get(name__iexact=source)
#   # except Source.DoesNotExist:
#   #           # Create new source if it doesn't exist
#   #           source = Source.objects.create(name=source)


#   Income.objects.create(owner=request.user,amount=amount,date=date,source=source,description=description) 
#   expenses=Income.objects.filter(owner=request.user)
#   context={
#   'source':source
#   }
#   messages.success(request,'Income saved succesfully!!')
#   return redirect('income')
class add_income(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({"message": "Income saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @login_required(login_url='/authentication/login')
# def edit_income(request,id):
#  income=Income.objects.get(pk=id)
#  sources = [
#     ("Salary", "Salary"),
#     ("Side Job", "Side Job"),
#     ("Business", "Business"),
#   ]
#  #sources= Source.objects.all()
#  context={
#   'income':income,
#   'values':income,
#   'sources':sources
  
#  }

#  if request.method=='GET':
#   return render(request,'income/edit_income.html',context)
#  if request.method=='POST':
#   amount=request.POST['amount']
#   description=request.POST['description']  
#   date=request.POST['dateOfIncome'] 
#   source=request.POST['source']

#   if not amount :
#    messages.error(request,"Amount is required")
#    return render(request,'income/edit_expense.html',context)
  

#   if not description :
#     messages.error(request,"Description is required")
#     return render(request,'income/edit_expense.html',context)
  
#   if not date :
#     messages.error(request,"Description is required")
#     return render(request,'income/edit_expense.html',context)
  
#   if not source :
#     messages.error(request,"Description is required")
#     return render(request,'income/edit_expense.html',context)
#   # try:
         
#   #           source = Source.objects.get(name__iexact=source)
#   # except Source.DoesNotExist:
            
#   #           source = Source.objects.create(name=source)
  
  


#   income.owner=request.user
#   income.amount= amount
#   income.date= date
#   income.source=source
#   income.description=description
#   income.save()
#   messages.success(request,'Expense updated successfully')

#   return redirect('income')
class edit_income(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        income = get_object_or_404(Income, pk=id, owner=request.user)
        serializer = IncomeSerializer(income)
        return Response({
            'income': serializer.data,
        })

    def put(self, request, id):
        income = get_object_or_404(Income, pk=id, owner=request.user)
        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({"message": "Income updated successfully!", "income": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# def delete_income(request,id):
#   income=Income.objects.get(pk=id)  
#   income.delete()
#   messages.success(request,'Income record removed')
#   return Response('income')
class delete_income(APIView):
    def delete(self, request, id):
        try:
            income = Income.objects.get(pk=id)
        except Income.DoesNotExist:
            raise NotFound('Income record not found')

        income.delete()
        return Response({'message': 'Income record removed'}, status=status.HTTP_204_NO_CONTENT)



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



