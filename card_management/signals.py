from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import CardOrder, Card


@receiver(post_save, sender=CardOrder)
def update_card_total_orders_on_save(sender, instance, created, **kwargs):
    """Update card total_orders when a new order is created or quantity changes"""
    card = instance.card
    
    if created:
        # New order - increment total_orders
        card.total_orders += instance.quantity
        card.save(update_fields=['total_orders'])
        
        # Send email notification to user
        send_order_confirmation_email(instance)
    else:
        # Existing order - check if quantity changed
        if instance.tracker.has_changed('quantity'):
            # Get the old quantity from the tracker
            old_quantity = instance.tracker.previous('quantity') or 0
            quantity_difference = instance.quantity - old_quantity
            
            # Update total_orders based on the difference
            card.total_orders += quantity_difference
            card.save(update_fields=['total_orders'])
        
        # Check if status has changed
        if instance.tracker.has_changed('status'):
            # Send status update email
            send_order_status_update_email(instance)


@receiver(post_delete, sender=CardOrder)
def update_card_total_orders_on_delete(sender, instance, **kwargs):
    """Decrease card total_orders when an order is deleted"""
    # Decrease total_orders for the card
    card = instance.card
    card.total_orders = max(0, card.total_orders - instance.quantity)
    card.save(update_fields=['total_orders'])


def send_order_confirmation_email(order):
    """Send order confirmation email to user"""
    try:
        subject = f"Order Confirmation - {order.card.name}"
        
        # Prepare email context
        context = {
            'order': order,
            'user': order.user,
            'card': order.card,
            'order_number': order.id,
            'total_amount': order.total_amount,
            'quantity': order.quantity,
            'order_date': order.order_date,
            'status': order.get_status_display(),
        }
        
        # Render email templates
        html_message = render_to_string('card_management/emails/order_confirmation.html', context)
        plain_message = render_to_string('card_management/emails/order_confirmation.txt', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Order confirmation email sent to {order.user.email}")
        
    except Exception as e:
        print(f"Failed to send order confirmation email: {str(e)}")


def send_order_status_update_email(order):
    """Send order status update email to user"""
    try:
        subject = f"Order Status Update - {order.card.name} (Order #{order.id})"
        
        # Prepare email context
        context = {
            'order': order,
            'user': order.user,
            'card': order.card,
            'order_number': order.id,
            'status': order.get_status_display(),
            'order_date': order.order_date,
        }
        
        # Render email templates
        html_message = render_to_string('card_management/emails/order_status_update.html', context)
        plain_message = render_to_string('card_management/emails/order_status_update.txt', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Order status update email sent to {order.user.email}")
        
    except Exception as e:
        print(f"Failed to send order status update email: {str(e)}") 