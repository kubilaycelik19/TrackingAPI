from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2 ,verbose_name="Fiyat")
    description = models.CharField(max_length=100, verbose_name="Açıklama")
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.amount} ₺"
    
# shell modunda category ekleme => Category.objects.create(name="Kategori Adı")
# shell modunda expense ekleme => Expense.objects.create(user_id=1, category_id=1, amount=100.50, description="Açıklama", date="2024-06-01")
# shell modunda expense listeleme => Expense.objects.all()
