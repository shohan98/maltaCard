from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Card, CardOrder
from authentication.models import UserProfile

@login_required
def card_list(request):
    """Display available cards"""
    cards = Card.objects.filter(is_active=True)
    context = {
        'cards': cards,
        'virtual_cards': cards.filter(card_type='virtual'),
        'physical_cards': cards.filter(card_type='physical'),
    }
    return render(request, 'card_management/card_list.html', context)

@login_required
def order_card(request, card_id):
    """Order a card"""
    card = get_object_or_404(Card, id=card_id, is_active=True)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Create order
        order = CardOrder.objects.create(
            user=request.user,
            card=card,
            quantity=quantity,
            total_amount=card.price * quantity
        )
        
        # If it's a physical card, add shipping information
        if card.card_type == 'physical':
            order.shipping_address = request.POST.get('shipping_address', '')
            order.city = request.POST.get('city', '')
            order.state = request.POST.get('state', '')
            order.postal_code = request.POST.get('postal_code', '')
            order.country = request.POST.get('country', '')
            order.phone_number = request.POST.get('phone_number', '')
            order.save()
        
        messages.success(request, f'Order placed successfully! Order #{order.id}')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'card': card,
        'user_profile': request.user.profile,
    }
    return render(request, 'card_management/order_card.html', context)

@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(CardOrder, id=order_id, user=request.user)
    return render(request, 'card_management/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    """View user's orders"""
    orders = CardOrder.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'card_management/my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(CardOrder, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel order. It is already being processed.')
    
    return redirect('my_orders')
