from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date', 'category']

    def validate(self, data):
        if not data.get('amount'):
            raise serializers.ValidationError({"amount": "Amount is required."})
        if not data.get('description'):
            raise serializers.ValidationError({"description": "Description is required."})
        if not data.get('date'):
            raise serializers.ValidationError({"date": "Date is required."})
        if not data.get('category'):
            raise serializers.ValidationError({"category": "Category is required."})
        return data

