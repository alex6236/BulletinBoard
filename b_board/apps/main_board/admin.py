from django.contrib import admin
from .models import Ad, Category, Reply, Subscription  #, Like, Dislike


class AdAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title', 'category_ad', 'rating', 'slug', 'time_create')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    def rating(self, obj):
        return obj.likes.count()
    
    rating.short_description = 'Рейтинг'
    

class CategoryAdmin(admin.ModelAdmin):
    
    def number_of_subscribers(self, obj):
        subscribers = Subscription.objects.filter(categories=obj).select_related('user')
        return subscribers.count()

    number_of_subscribers.short_description = 'Количество подписчиков'
    
    list_display = ('id', 'name', 'number_of_subscribers', 'slug')
    list_display_links = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
class SubscriptionAdmin(admin.ModelAdmin):
    
    def sub_categories(self, obj):
        return ', '.join([str(category) for category in obj.categories.all()])
    
    sub_categories.short_description = 'Подписки пользователя'
    
    list_display = ('id', 'user', 'sub_categories')
    list_filter = ('user', 'categories')
    
class ReplyAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'author', 'text', 'is_published', 'created_reply')
    list_filter = ('author', 'is_published')

admin.site.register(Ad, AdAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

