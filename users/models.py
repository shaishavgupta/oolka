from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    
    def __str__(self):
        return f'{self.email}-{self.name}-{self.is_active}'
    
    def is_valid(self):
        return self.is_active