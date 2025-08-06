from django.core.management.base import BaseCommand
from card_management.models import Card


class Command(BaseCommand):
    help = 'Recalculate total_orders for all cards based on actual order quantities'

    def handle(self, *args, **options):
        self.stdout.write('Starting to recalculate card total_orders...')
        
        cards = Card.objects.all()
        updated_count = 0
        
        for card in cards:
            old_total = card.total_orders
            new_total = card.recalculate_total_orders()
            
            if old_total != new_total:
                self.stdout.write(
                    f'Card "{card.name}": {old_total} -> {new_total} orders'
                )
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully recalculated total_orders for {updated_count} cards'
            )
        ) 