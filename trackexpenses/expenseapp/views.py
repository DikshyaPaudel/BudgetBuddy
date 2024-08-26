from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from income.models import Income,Source
from django.contrib import messages
from django.core.paginator import Paginator
import json #you  can get everything that the user is trying to search for
from django.http import JsonResponse
#we get data as json and convert into python dictionarty in the same way to send  data back to user in json we use http response
# Create your views here.
import datetime
from django.core import serializers
from django.db.models import Sum
from django.shortcuts import get_object_or_404


from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


def search_expenses(request):
 if request.method=='POST':
  search_str=json.loads(request.body).get('searchText') #json.loads convert the json obtained from request.body to python dictionary
  expenses=Expense.objects.filter(amount__istartswith=search_str,owner=request.user) | Expense.objects.filter(description__icontains=search_str,owner=request.user) | Expense.objects.filter(date__istartswith=search_str,owner=request.user) | Expense.objects.filter(category__icontains=search_str,owner=request.user)
  # second parameter is used so that onnly the expense that particualar user has added to expense and not other user expenses will be displayed
  # in expenses variable we now have a query set

  data=expenses.values()
  return JsonResponse(list(data),safe=False) #safe=false allows that allows jsonresponse class to be pass something that is not dictionary easily

# @login_required(login_url='/authentication/login')
# def index(request):
#  categories=  Category.objects.all()
#  expenses=Expense.objects.filter(owner=request.user) #all the expenses of that particular user
#  paginator=Paginator(expenses,3) #pass two parameters i.e one is the object that we want to paginate and another is number of item to be displayed in a page
#  page_number=request.GET.get('page' ) #total page number 
#  #GET.get
#  page_obj=paginator.get_page(page_number) # which data to display in that page number  
#  totalpage=page_obj.paginator.num_pages; #num_pages gives total number of pages
#  context={
#   'expenses':expenses,
#   'page_obj':page_obj,
#   'totalpageList': [n+1 for n in range(totalpage)],
#   'totalpage':totalpage
#  }
#  return render(request,'index.html',context)

class index(APIView):

    def get(self, request):
        expenses = Expense.objects.filter(owner=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        
        return Response(serializer.data)



# def add_expense(request):
#  categories = [
#     ("Health", "Health"),
#     ("Insurance", "Insurance"),
#     ("Education", "Education"),
#     ("Fuel", "Fuel"),
#     ("Groceries", "Groceries"),
#     ("Electricity", "Electricity"),
#     ("Internet","Internet"),
#     ("Airlines","Airlines"),
#     ("Others","Others")
#   ] 
# # categories=  Category.objects.all()
#  context={
#   'categories':categories,
#   'values':request.POST
#  }
#  if request.method=='GET':
#    return render(request,'add_expense.html',context)

#  if request.method=='POST':
#   amount=request.POST['amount']
#   description=request.POST['description']  
#   date=request.POST['dateOfExpense'] 
#   category=request.POST['category']

#   if not amount :
#    messages.error(request,"Amount is required")
#    return render(request,'add_expense.html',context)
  
#   if not description :
#     messages.error(request,"Description is required")
#     return render(request,'add_expense.html',context)
  
#   if not date :
#     messages.error(request,"All the fields are required")
#     return render(request,'add_expense.html',context)
  
#   if not category :
#     messages.error(request,"All the fields are required")
#     return render(request,'add_expense.html',context)
#   # try:
#   #           # Check for existing category (case-insensitive)
#   #           category = Category.objects.get(name__iexact=category)
#   # except Category.DoesNotExist:
#   #           # Create new category if it doesn't exist
#   #           category = Category.objects.create(name=category)
  
#   Expense.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description) #if owner is not included then it shows eror because owner is defined inside in model and we need to save data inside the owner  too
#   expenses=Expense.objects.filter(owner=request.user)
#   context={
#   'expenses':expenses
#   }
#   messages.success(request,'Expense saved succesfully!!')
#   return redirect('expenses')
  # return render(request,'index.html',context)
class add_expense(APIView):

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({"message": "Expense saved successfully!", "expense": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#EDIT

# def edit_expense(request,id):
#  expense=Expense.objects.get(pk=id)
#  #categories= Category.objects.all()
#  categories = [
#     ("Health", "Health"),
#     ("Insurance", "Insurance"),
#     ("Education", "Education"),
#     ("Fuel", "Fuel"),
#     ("Groceries", "Groceries"),
#     ("Electricity", "Electricity"),
#     ("Internet","Internet"),
#     ("Airlines","Airlines"),
#     ("Others","Others")
#   ] 
#  context={
#   'expense':expense,
#   'values':expense,
#   'categories':categories
  
#  }

#  if request.method=='GET':
#   return render(request,'edit_expense.html',context)
#  if request.method=='POST':
#   amount=request.POST['amount']
#   description=request.POST['description']  
#   date=request.POST['dateOfExpense'] 
#   category=request.POST['category']

#   if not amount :
#    messages.error(request,"Amount is required")
#    return render(request,'edit_expense.html',context)
  

#   if not description :
#     messages.error(request,"Description is required")
#     return render(request,'edit_expense.html',context)
#   if not date :
#     messages.error(request,"All the fields are required")
#     return render(request,'edit_expense.html',context)
#   if not category :
#     messages.error(request,"All the fields are required")
#     return render(request,'edit_expense.html',context)
#   # try:
#   #           category = Category.objects.get(name__iexact=category)
#   # except Category.DoesNotExist:
#   #           # Create new category with uppercase name (optional)
#   #           category = Category.objects.create(name=category.upper())

  

#   expense.owner=request.user
#   expense.amount= amount
#   expense.date= date
#   expense.category=category
#   expense.description=description
#   expense.save()
#   messages.success(request,'Expense updated successfully')

#   return redirect(index)

class edit_expense(APIView):

    def get(self, request, id):
        expense = get_object_or_404(Expense, pk=id, owner=request.user)
        serializer = ExpenseSerializer(expense)
        return Response({
            'expense': serializer.data,
        })

    def put(self, request, id):
        expense = get_object_or_404(Expense, pk=id, owner=request.user)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Expense updated successfully!", "expense": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
# def delete_expense(request,id):
#   expense=Expense.objects.get(pk=id)  
#   expense.delete()
#   messages.success(request,'Expense removed')
#   return redirect(index)
class delete_expense(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        expense = get_object_or_404(Expense, pk=id, owner=request.user)
        expense.delete()
        return Response({"message": "Expense removed successfully!"}, status=status.HTTP_204_NO_CONTENT)


def expense_category_summary(request):
 today_date=datetime.date.today()
 three_months_ago=today_date-datetime.timedelta(days=30*3) 
 expense=Expense.objects.filter(owner=request.user,date__gte=three_months_ago,date__lte=today_date)
 finalrep={}

 def get_category(expense):
  return expense.category

 category_list=list(set(map(get_category,expense)))

 def get_expense_category_amount(category):
  amount=0;
  filtered_by_category=expense.filter(category=category) 
  for item in filtered_by_category:
   amount+=item.amount
  return amount

 for x in expense:
  for y in category_list:
   finalrep[y]=get_expense_category_amount(y)
 total_sum=sum(finalrep.values())
 combined={'expense_category_data':finalrep,
            'total_sum':total_sum
        
     }

 return JsonResponse(combined,safe=False)

def stats(request):
 return render(request,'stats.html')




def income_source_summary(request):
    today_date = datetime.date.today()
    three_months_ago = today_date - datetime.timedelta(days=30*3) 
    income = Income.objects.filter(owner=request.user, date__gte=three_months_ago, date__lte=today_date)

    finalrep = {}
    source_list = set(income.values_list('source', flat=True))

    def get_income_source_amount(source):
        filtered_by_source = income.filter(source=source)
        amount = sum(item.amount for item in filtered_by_source)
        return amount

    for source in source_list:
        finalrep[source] = get_income_source_amount(source)

    total_sum = sum(finalrep.values())

    combined = {
        'income_category_data': finalrep,
        'total_sum': total_sum
    }

    return JsonResponse(combined, safe=False)
