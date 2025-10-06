from django.core.management.base import BaseCommand
from django.core.files import File
import os
from core.models import Room, RoomImage
from django.conf import settings


class Command(BaseCommand):
    help = 'Link existing images in media folder to rooms'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Linking existing images to rooms...'))
        
        # Get all rooms
        rooms = Room.objects.all()
        if not rooms.exists():
            self.stdout.write(self.style.WARNING('No rooms found. Create some rooms first.'))
            return
        
        # Get all image files in room_images folder
        room_images_dir = os.path.join(settings.MEDIA_ROOT, 'room_images')
        if not os.path.exists(room_images_dir):
            self.stdout.write(self.style.WARNING('Room images directory does not exist.'))
            return
        
        image_files = [f for f in os.listdir(room_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        if not image_files:
            self.stdout.write(self.style.WARNING('No image files found in room_images directory.'))
            return
        
        self.stdout.write(f'Found {len(image_files)} image files')
        self.stdout.write(f'Found {rooms.count()} rooms')
        
        # Link images to rooms
        images_created = 0
        for i, room in enumerate(rooms):
            # Assign 2-3 images per room
            images_per_room = min(3, len(image_files) // rooms.count() + 1)
            room_images = image_files[i * images_per_room:(i + 1) * images_per_room]
            
            for j, image_file in enumerate(room_images):
                image_path = os.path.join(room_images_dir, image_file)
                
                # Create RoomImage instance
                with open(image_path, 'rb') as f:
                    django_file = File(f, name=image_file)  # Use just the filename
                    room_image = RoomImage.objects.create(
                        room=room,
                        image=django_file,
                        is_primary=(j == 0),  # First image is primary
                        caption=f"Room image {j + 1}"
                    )
                    images_created += 1
                    self.stdout.write(f'Created image for room "{room.title}": {image_file}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {images_created} room images!'))
        
        # Verify results
        total_images = RoomImage.objects.count()
        rooms_with_images = Room.objects.filter(images__isnull=False).distinct().count()
        
        self.stdout.write(f'Total room images in database: {total_images}')
        self.stdout.write(f'Rooms with images: {rooms_with_images}')
