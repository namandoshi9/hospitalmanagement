from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Medicine
import random
import string
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import os

@receiver(post_save, sender=Medicine)
def generate_barcode(sender, instance, created, **kwargs):
    if created and not instance.barcode:
        # Generate a random 12-digit numeric string for the barcode
        barcode_value = ''.join(random.choices(string.digits, k=12))

        # Generate barcode using python-barcode library
        ean = barcode.get_barcode_class('ean13')
        code = ean(barcode_value, writer=ImageWriter())

        # Save barcode to BytesIO buffer
        buffer = BytesIO()
        code.write(buffer)

        # Create filename
        filename = f'{barcode_value}.png'
        filepath = os.path.join('barcodes', filename)

        # Ensure the directory exists before saving the file
        if not os.path.exists('barcodes'):
            os.makedirs('barcodes')

        # Save barcode image to ImageField
        instance.barcode.save(filename, File(buffer), save=True)

        # Update the instance to save the changes
        instance.save()
