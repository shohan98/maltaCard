# Card Order Features Implementation

## Overview
This document outlines the automatic features implemented for card orders in the MaltaCard application.

## Features Implemented

### 1. Automatic Total Orders Tracking

#### **Card Order Creation**
- ✅ **Increment**: When a new `CardOrder` is created, the `total_orders` field of the associated `Card` is automatically incremented by the order quantity
- ✅ **Signal**: Uses Django signals (`post_save`) to detect new order creation
- ✅ **Thread-safe**: Uses `update_fields` to ensure atomic updates

#### **Card Order Deletion**
- ✅ **Decrement**: When a `CardOrder` is deleted, the `total_orders` field of the associated `Card` is automatically decremented by the order quantity
- ✅ **Signal**: Uses Django signals (`post_delete`) to detect order deletion
- ✅ **Safety**: Ensures `total_orders` never goes below 0

### 2. Email Notifications

#### **Order Confirmation Email**
- ✅ **Trigger**: Sent automatically when a new order is created
- ✅ **Content**: Includes order details, user information, and confirmation message
- ✅ **Templates**: Both HTML and plain text versions available
- ✅ **Styling**: Professional email design with MaltaCard branding

#### **Order Status Update Email**
- ✅ **Trigger**: Sent automatically when order status changes
- ✅ **Content**: Includes updated status and order details
- ✅ **Templates**: Both HTML and plain text versions available
- ✅ **Field Tracking**: Uses `django-model-utils` FieldTracker to detect status changes

## Technical Implementation

### Files Created/Modified

#### **Models**
- `card_management/models.py`: Added FieldTracker for status change detection

#### **Signals**
- `card_management/signals.py`: New file with signal handlers
- `card_management/apps.py`: Updated to register signals

#### **Email Templates**
- `templates/card_management/emails/order_confirmation.html`
- `templates/card_management/emails/order_confirmation.txt`
- `templates/card_management/emails/order_status_update.html`
- `templates/card_management/emails/order_status_update.txt`

#### **Settings**
- `maltaCard/settings.py`: Added email configuration
- `requirements.txt`: Added `django-model-utils==4.3.1`

#### **Tests**
- `card_management/tests.py`: Comprehensive test coverage
- `card_management/management/commands/test_email.py`: Test command

### Signal Handlers

```python
@receiver(post_save, sender=CardOrder)
def update_card_total_orders_on_save(sender, instance, created, **kwargs):
    """Update card total_orders when a new order is created or status changes"""
    if created:
        # Increment total_orders for the card
        card = instance.card
        card.total_orders += instance.quantity
        card.save(update_fields=['total_orders'])
        
        # Send email notification to user
        send_order_confirmation_email(instance)
    else:
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
```

## Email Configuration

### Development Mode
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@maltacard.com'
```

### Production Mode (Uncomment in settings.py)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Testing

### Running Tests
```bash
# Run all card order tests
python manage.py test card_management.tests.CardOrderTestCase

# Test email functionality
python manage.py test_email --email your-email@example.com
```

### Test Coverage
- ✅ Card total_orders increment on order creation
- ✅ Card total_orders decrement on order deletion
- ✅ Card total_orders never goes below zero
- ✅ Order confirmation email sent on creation
- ✅ Order status update email sent on status change
- ✅ No email sent on other field changes
- ✅ Order total amount calculation
- ✅ Multiple orders affect total_orders correctly

## Usage Examples

### Creating an Order (API)
```bash
POST /api/cards/orders/
{
    "user": 1,
    "card": 1,
    "quantity": 2,
    "shipping_address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "postal_code": "10001",
    "phone_number": "+1234567890"
}
```

### Updating Order Status (API)
```bash
PATCH /api/cards/orders/1/
{
    "status": "processing"
}
```

### Deleting an Order (API)
```bash
DELETE /api/cards/orders/1/
```

## Benefits

1. **Automatic Tracking**: No manual intervention required for total_orders updates
2. **Email Notifications**: Users stay informed about their orders
3. **Data Integrity**: Ensures total_orders is always accurate
4. **Professional Communication**: Branded email templates
5. **Comprehensive Testing**: Full test coverage ensures reliability
6. **Scalable**: Works with any number of orders and cards

## Future Enhancements

1. **Email Templates**: Add more email templates for different scenarios
2. **SMS Notifications**: Add SMS notifications for critical updates
3. **Email Preferences**: Allow users to configure notification preferences
4. **Order History**: Track order status change history
5. **Analytics**: Add analytics for order patterns and trends 