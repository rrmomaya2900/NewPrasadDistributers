from django.db import models
import time
import os

class GSTDeclaration(models.Model):
    gst_number = models.CharField(max_length=15, unique=True, primary_key=True)
    year_of_filing = models.CharField()
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    office_mobile_number = models.CharField(max_length=10)
    personal_mobile_number = models.CharField(max_length=10)
    pan_number = models.CharField(max_length=10, unique=True)
    company_email_address = models.EmailField(max_length=254, unique=True)
    drug_license_number20b = models.CharField(max_length=20, blank=True, null=True)
    drug_license_validity20b = models.DateField(blank=True, null=True)
    drug_license_number21b = models.CharField(max_length=20, blank=True, null=True)
    drug_license_validity21b = models.DateField(blank=True, null=True)
    drug_license_number20d = models.CharField(max_length=20, blank=True, null=True)
    drug_license_validity20d = models.DateField(blank=True, null=True)
    tan_number = models.CharField(max_length=10, blank=True, null=True)
    turnover = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')])
    tds_tcs = models.CharField(max_length=3, choices=[('tds', 'TDS'), ('tcs', 'TCS')], blank = True)
    
    # S3 image/file links storage
    customer_photo = models.ImageField(upload_to='gst/customer_photo/')
    gst_certification_photo = models.ImageField(upload_to='gst/gst_certification_photo/')
    udyan_adhar_photo = models.ImageField(upload_to='gst/udyan_adhar_photo/')
    personal_pan_photo = models.ImageField(upload_to='gst/personal_pan_photo/')
    personal_adhar_photo = models.ImageField(upload_to='gst/personal_adhar_photo/')
    drug_license_photo20b = models.ImageField(upload_to='gst/drug_license_photo20b/')
    drug_license_photo21b = models.ImageField(upload_to='gst/drug_license_photo21b/')
    drug_license_photo20d = models.ImageField(upload_to='gst/drug_license_photo20d/')
    food_license_photo = models.ImageField(upload_to='gst/food_license_photo/')
    shop_photo = models.ImageField(upload_to='gst/shop_photo/')

    # PDF URL field
    acknowledgement_pdf_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name