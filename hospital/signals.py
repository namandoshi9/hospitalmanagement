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
import random
import string
# @receiver(post_save, sender=Medicine)
# def generate_barcode(sender, instance, created, **kwargs):
#     if created and not instance.barcode:
#         # Generate a random 12-digit numeric string for the barcode
        

#         bar = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#         # Generate a barcode by selecting random digits from the list 'bar' and additional random digits
#         barcode_value = ''.join([str(random.choice(bar)) for _ in range(5)])  # Assuming you want 5 random digits from the list
#         barcode_value += ''.join(random.choices(string.digits, k=8))

       
#         # if barcode_value.startswith('0'):
#         #     barcode_value = '1' + barcode_value[1:]

#         # Generate barcode using python-barcode library
#         ean = barcode.get_barcode_class('ean13')
#         code = ean(barcode_value, writer=ImageWriter())

#         # Save barcode to BytesIO buffer
#         buffer = BytesIO()
#         code.write(buffer)

#         # Create filename
#         filename = f'{barcode_value}.png'
#         filepath = os.path.join('barcodes', filename)

#         # Ensure the directory exists before saving the file
#         if not os.path.exists('barcodes'):
#             os.makedirs('barcodes')

#         # Save barcode image to ImageField
#         instance.barcode.save(filename, File(buffer), save=True)

#         # Save barcode value to the model
#         instance.barcode_value = barcode_value
#         instance.save()

# digits = list(range(1, 10))

@receiver(post_save, sender=Medicine)
def generate_barcode(sender, instance, created, **kwargs):
    if created and not instance.barcode:
        # Generate a random 12-digit numeric string for the barcode
        barcode_value = ''.join(random.choices(string.digits, k=12))

        if barcode_value.startswith('0'):
            barcode_value = '1' + barcode_value[1:]

        # if barcode_value.startswith('0'):
        #     barcode_value = barcode_value.lstrip('0')

        # Generate barcode using python-barcode library
        ean = barcode.get_barcode_class('ean13')

        print(ean)
        code = ean(barcode_value, writer=ImageWriter())
        print(code)

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

        # Save barcode value to the model
        instance.barcode_value = code
        instance.save()

        