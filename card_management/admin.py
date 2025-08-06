from django.contrib import admin
from .models import Card, CardOrder, CardType

@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_type', 'price', 'is_popular', 'sort_order', 'is_active', 'created_at')
    list_filter = ('duration_type', 'is_popular', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_popular', 'sort_order', 'is_active', 'price')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'duration_type', 'price', 'is_popular', 'sort_order', 'is_active')
        }),
        ('Limits and Features', {
            'fields': ('max_transactions', 'daily_limit', 'monthly_limit', 'features'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('sort_order', 'name') 
    

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_type', 'price', 'is_active', 
                    'total_orders', 'created_at')
    list_filter = ('card_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'price')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'card_type', 'description', 'price', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CardOrder)
class CardOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card', 'quantity', 'total_amount', 'status', 'order_date')
    list_filter = ('status', 'card__card_type', 'order_date')
    search_fields = ('user__username', 'user__email', 'card__name')
    readonly_fields = ('order_date', 'updated_at', 'total_amount')
    list_editable = ('status',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'card', 'quantity', 'total_amount', 'status')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'city', 'state', 'postal_code', 'country', 'phone_number'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('order_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'card')
