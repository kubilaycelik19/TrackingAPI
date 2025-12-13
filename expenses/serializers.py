from rest_framework import serializers
from .models import Expense, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'date', 'category', 'category_name', 'user']
        read_only_fields = ['user']


class ReceiptAnalysisSerializer(serializers.Serializer):
    receipt_image = serializers.ImageField(required=True, help_text="Yüklenecek fiş görseli (JPG/PNG)")