# rooms/management/commands/seed_rooms.py
import random
from django.core.management.base import BaseCommand
from faker import Faker
from rooms.models import Room, RoomImage

class Command(BaseCommand):
    help = "Создает тестовые комнаты и фото"

    def handle(self, *args, **options):
        fake = Faker("ru_RU")

        room_types = ['standard', 'superior', 'suite']
        statuses = ['available', 'occupied', 'reserved']

        created_rooms = 0

        for i in range(1, 11):
            room_number = str(100 + i)

            room, created = Room.objects.get_or_create(
                room_number=room_number,
                defaults={
                    'room_type': random.choice(room_types),
                    'price_per_day': random.randint(3000, 15000),
                    'capacity': random.randint(1, 4),
                    'status': random.choice(statuses),
                }
            )

            if created:
                created_rooms += 1

                for j in range(random.randint(2, 5)):
                    RoomImage.objects.create(
                        room=room,
                        image=f"rooms/demo_{i}_{j+1}.jpg",
                        alt_text=f"Фото комнаты {room.room_number}"
                    )

        self.stdout.write(self.style.SUCCESS(f"Готово! Создано комнат: {created_rooms}"))