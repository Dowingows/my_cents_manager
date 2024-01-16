import os

from django.core.exceptions import ValidationError


class FileExtensionValidator:
    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(
                'Unsupported file extension. Please use a PDF, PNG, JPEG or JPG file.'
            )
