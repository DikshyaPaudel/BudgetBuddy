from rest_framework import serializers
from .models import Income

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount', 'description', 'date', 'source']

    def validate(self, data):
        if not data.get('amount'):
            raise serializers.ValidationError({"amount": "Amount is required."})
        if not data.get('description'):
            raise serializers.ValidationError({"description": "Description is required."})
        if not data.get('date'):
            raise serializers.ValidationError({"date": "Date is required."})
        if not data.get('source'):
            raise serializers.ValidationError({"source": "Source is required."})
        return data
