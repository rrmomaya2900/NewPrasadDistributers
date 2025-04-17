from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import GSTDeclaration
from io import BytesIO
import openpyxl


# Admin Action for Excel Download
@admin.action(description="Download selected as Excel")
def download_selected_excel(modeladmin, request, queryset):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "GST Declarations"

    headers = [
        'GST Number', 'Year of Filing', 'Company Name',
        'PAN Card Number', 'Drug License20B Number',
        'Drug License21B Number', 'Drug License20D Number', 'TAN Number',
    ]
    sheet.append(headers)

    for obj in queryset:
        row = [
            obj.gst_number,
            obj.year_of_filing,
            obj.company_name,
            obj.pan_number,
            obj.drug_license_number20b,
            obj.drug_license_number21b,
            obj.drug_license_number20d,
            obj.tan_number
        ]
        sheet.append(row)

    # Write workbook to memory
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Return response
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Selected_GST_Entries.xlsx'
    return response


# Register the Admin
@admin.register(GSTDeclaration)
class GSTDeclarationAdmin(admin.ModelAdmin):
    list_display = (
        'gst_number',
        'company_name',
        'year_of_filing',
        'city',
        'state',
        'office_mobile_number',
        'personal_mobile_number',
        'pan_number',
        'company_email_address',
        'drug_license_number20b',
        'drug_license_number21b',
        'drug_license_number20d',
        'tan_number',
        'turnover',
        'tds_tcs',
        'customer_photo',
        'gst_certification_photo',
        'udyan_adhar_photo',
        'personal_pan_photo',
        'personal_adhar_photo',
        'drug_license_photo20b',
        'drug_license_photo21b',
        'drug_license_photo20d',
        'food_license_photo',
        'shop_photo',
        'acknowledgement_pdf_link',  # Replaced raw URL field
    )
    search_fields = ('gst_number', 'company_name', 'pan_number')
    list_filter = ('state', 'year_of_filing')
    readonly_fields = (
        'customer_photo',
        'gst_certification_photo',
        'udyan_adhar_photo',
        'personal_pan_photo',
        'personal_adhar_photo',
        'drug_license_photo20b',
        'drug_license_photo21b',
        'drug_license_photo20d',
        'food_license_photo',
        'shop_photo',
        'acknowledgement_pdf_url'
    )
    actions = [download_selected_excel]

    def acknowledgement_pdf_link(self, obj):
        if obj.acknowledgement_pdf_url:
            return format_html(
                '<a href="{}" target="_blank">View PDF</a>',
                obj.acknowledgement_pdf_url
            )
        return "-"
    acknowledgement_pdf_link.short_description = "Acknowledgement PDF"