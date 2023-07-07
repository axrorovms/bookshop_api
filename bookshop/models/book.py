from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
import os
from .base import upload_name, BaseModel
from Bookshop_project.settings import BASE_DIR
from pdf2image import convert_from_path


class Category(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Author(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Book(BaseModel):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_name, blank=True, null=True)
    page_pdf = models.FileField(
        upload_to=upload_name, validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )
    price = models.DecimalField(max_digits=30, decimal_places=2)
    page_count = models.IntegerField(default=0)
    year = models.CharField(max_length=4)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def set_page_book(self):
        import pdfplumber
        with pdfplumber.open(self.page_pdf.file) as pdf:
            self.page_count = len(pdf.pages)

    def get_image_url(self):
        from uuid import uuid4
        image_url = f"{upload_name(self, f'{uuid4()}.jpg')}"
        return image_url

    def get_pdf_url(self):
        return self.page_pdf.url

    def convert_pdf_to_jpg(self, pdf_url, image_url, image_name):
        url_pdf = f"{BASE_DIR}/{pdf_url}"
        url_jpg = f"{BASE_DIR}/media/{image_url}"
        if not os.path.exists(url_jpg):
            os.makedirs(url_jpg)
            convert_from_path(
                pdf_path=url_pdf,
                dpi=500,
                output_folder=url_jpg,
                output_file=image_name,
                fmt="jpeg",
                first_page=1,
                single_file=True
            )
        else:
            convert_from_path(
                pdf_path=url_pdf,
                dpi=500,
                output_folder=url_jpg,
                output_file=image_name,
                fmt="jpeg",
                first_page=1,
                single_file=True
            )

    def convert_pdf_to_image(self):
        pdf_url = self.get_pdf_url()
        image_url = self.get_image_url()
        img_name = image_url.split('/')[-1]
        img_url = "/".join(image_url.split('/')[0:-1]) + '/'
        self.convert_pdf_to_jpg(pdf_url, img_url, img_name)

        return image_url

    def save(self, *args, **kwargs):
        self.set_page_book()
        if not self.image or self.image == 'null':
            super().save(*args, **kwargs)
            self.image = self.convert_pdf_to_image()
            return self.save()
        super().save(*args, **kwargs)


