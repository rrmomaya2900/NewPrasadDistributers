import io
import datetime
import boto3
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import GSTForm
from .models import GSTDeclaration
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import GSTDeclarationSerializer
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from django.template.loader import get_template
from django.template.loader import render_to_string
from xhtml2pdf import pisa 
from datetime import datetime
from io import BytesIO
from GST_app.models import GSTDeclaration
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
from .models import GSTDeclaration

# Home Page
def home(request):
    return render(request, 'home.html')

# View for GST Form (Template-Based Submission)
# def gst_form_view(request):
#     if request.method == 'POST':
#         form = GSTForm(request.POST, request.FILES)
#         if form.is_valid():
#             # 1. Save text data to GSTDeclaration
#             tds_tcs_value = 'tds' if form.cleaned_data['turnover'] == 'yes' else 'tcs'
            
#             # 1. Save text data to GSTDeclaration
#             gst_instance = GSTDeclaration.objects.create(
#                 gst_number=form.cleaned_data['gst_number'],
#                 year_of_filing=form.cleaned_data['year_of_filing'],
#                 company_name=form.cleaned_data['company_name'],
#                 company_address=form.cleaned_data['company_address'],
#                 city=form.cleaned_data['city'],
#                 state=form.cleaned_data['state'],
#                 pincode=form.cleaned_data['pincode'],
#                 office_mobile_number=form.cleaned_data['office_mobile_number'],
#                 personal_mobile_number=form.cleaned_data['personal_mobile_number'],
#                 pan_number=form.cleaned_data['pan_number'],
#                 company_email_address=form.cleaned_data['company_email_address'],
#                 drug_license_number20b=form.cleaned_data.get('drug_license_number20b'),
#                 drug_license_validity20b=form.cleaned_data.get('drug_license_validity20b'),
#                 drug_license_number21b=form.cleaned_data.get('drug_license_number21b'),
#                 drug_license_validity21b=form.cleaned_data.get('drug_license_validity21b'),
#                 drug_license_number20d=form.cleaned_data.get('drug_license_number20d'),
#                 drug_license_validity20d=form.cleaned_data.get('drug_license_validity20d'),
#                 tan_number=form.cleaned_data.get('tan_number'),
#                 turnover=form.cleaned_data['turnover'],
#                 tds_tcs = 'tds' if form.cleaned_data.get('turnover') == 'yes' else 'tcs',  # Set based on turnover
#             )
            
#             gst_number = form.cleaned_data['gst_number']
#             file_fields = [
#                 ('customer_photo', 'customer_photo.jpg'),
#                 ('gst_certification_photo', 'gst_certification.jpg'),
#                 ('udyan_adhar_photo', 'udyan_adhar.jpg'),
#                 ('personal_pan_photo', 'personal_pan.jpg'),
#                 ('personal_adhar_photo', 'personal_adhar.jpg'),
#                 ('drug_license_photo20b', 'drug_license_photo20b.jpg'),
#                 ('drug_license_photo21b', 'drug_license_photo21b.jpg'),
#                 ('drug_license_photo20d', 'drug_license_photo20d.jpg'),
#                 ('food_license_photo', 'food_license_photo.jpg'),
#                 ('shop_photo', 'shop_photo.jpg'),
#             ]
#             for field_name, file_name in file_fields:
#                 file = request.FILES.get(field_name)
#                 if file:
#                     upload_file_to_s3(file, f"{gst_number}/{file_name}")
            
            
#             customer_url = upload_file_to_s3(request.FILES['customer_photo'], f"{gst_number}/customer_photo.jpg")
#             gst_certification_url = upload_file_to_s3(request.FILES['gst_certification_photo'], f"{gst_number}/gst_certification.jpg")
#             udyan_adhar_url = upload_file_to_s3(request.FILES['udyan_adhar_photo'], f"{gst_number}/udyan_adhar.jpg")
#             personal_pan_url = upload_file_to_s3(request.FILES['personal_pan_photo'], f"{gst_number}/personal_pan.jpg")
#             personal_adhar_url = upload_file_to_s3(request.FILES['personal_adhar_photo'], f"{gst_number}/personal_adhar.jpg")
#             drug_license_url20b = upload_file_to_s3(request.FILES['drug_license_photo20b'], f"{gst_number}/drug_license_photo20b.jpg")
#             drug_license_url21b = upload_file_to_s3(request.FILES['drug_license_photo21b'], f"{gst_number}/drug_license_photo21b.jpg")
#             drug_license_url20d = upload_file_to_s3(request.FILES['drug_license_photo20d'], f"{gst_number}/drug_license_photo20d.jpg")
#             food_license_url = upload_file_to_s3(request.FILES['food_license_photo'], f"{gst_number}/food_license_photo.jpg")
#             shop_url = upload_file_to_s3(request.FILES['shop_photo'], f"{gst_number}/shop_photo.jpg")
            
#             gst_instance.customer_photo_url = customer_url
#             gst_instance.gst_certification_photo_url = gst_certification_url
#             gst_instance.udyan_adhar_photo_url = udyan_adhar_url
#             gst_instance.personal_pan_photo_url = personal_pan_url
#             gst_instance.personal_adhar_photo_url = personal_adhar_url
#             gst_instance.drug_license_photo_url20b = drug_license_url20b
#             gst_instance.drug_license_photo_url21b = drug_license_url21b
#             gst_instance.drug_license_photo_url20d = drug_license_url20d
#             gst_instance.food_license_photo_url = food_license_url
#             gst_instance.shop_photo_url = shop_url

#             gst_instance.save()


#             print("Redirecting to success page...")
#             # return redirect('success_page')
#             # return redirect(f'/success/?gst_number={gst_number}')
#             request.session['gst_number'] = gst_number
#             return redirect('success_page')
#         else:
#             print("Form Errors:", form.errors)

#     else:
#         form = GSTForm()

#     return render(request, 'form.html', {'form': form})

    
# @api_view(['POST'])
# def submit_gst_form(request):
#     print("Incoming Data:", request.data)
#     serializer = GSTDeclarationSerializer(data=request.data)

#     if serializer.is_valid():
#         instance = serializer.save()
#         gst_number = instance.gst_number
#         return Response({
#             "success": True,
#             "gst_number": instance.gst_number
#         })  # ✅ Send JSON instead of redirect

#     print("Serializer Errors:", serializer.errors)
#     return Response({
#         "success": False,
#         "errors": serializer.errors
#     }, status=status.HTTP_400_BAD_REQUEST)


# def success_page(request):
#     gst_number = request.GET.get('gst_number')  # or get it from the session if stored
#     return render(request, 'success.html', {'gst_number': gst_number})

def gst_form_view(request):
    if request.method == 'POST':
        form = GSTForm(request.POST, request.FILES)
        if form.is_valid():
            gst_number = form.cleaned_data['gst_number']

            # Save text data to GSTDeclaration
            gst_instance = GSTDeclaration.objects.create(
                gst_number=gst_number,
                year_of_filing=form.cleaned_data['year_of_filing'],
                company_name=form.cleaned_data['company_name'],
                company_address=form.cleaned_data['company_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
                office_mobile_number=form.cleaned_data['office_mobile_number'],
                personal_mobile_number=form.cleaned_data['personal_mobile_number'],
                pan_number=form.cleaned_data['pan_number'],
                company_email_address=form.cleaned_data['company_email_address'],
                drug_license_number20b=form.cleaned_data.get('drug_license_number20b'),
                drug_license_validity20b=form.cleaned_data.get('drug_license_validity20b'),
                drug_license_number21b=form.cleaned_data.get('drug_license_number21b'),
                drug_license_validity21b=form.cleaned_data.get('drug_license_validity21b'),
                drug_license_number20d=form.cleaned_data.get('drug_license_number20d'),
                drug_license_validity20d=form.cleaned_data.get('drug_license_validity20d'),
                tan_number=form.cleaned_data.get('tan_number'),
                turnover=form.cleaned_data['turnover'],
                tds_tcs='tds' if form.cleaned_data['turnover'] == 'yes' else 'tcs',
            )

            # File uploads to S3 and setting URL fields
            file_fields = {
                'customer_photo': 'customer_photo.jpg',
                'gst_certification_photo': 'gst_certification.jpg',
                'udyan_adhar_photo': 'udyan_adhar.jpg',
                'personal_pan_photo': 'personal_pan.jpg',
                'personal_adhar_photo': 'personal_adhar.jpg',
                'drug_license_photo20b': 'drug_license_photo20b.jpg',
                'drug_license_photo21b': 'drug_license_photo21b.jpg',
                'drug_license_photo20d': 'drug_license_photo20d.jpg',
                'food_license_photo': 'food_license_photo.jpg',
                'shop_photo': 'shop_photo.jpg',
            }

            for field_name, file_name in file_fields.items():
                file = request.FILES.get(field_name)
                if file:
                    url = upload_file_to_s3(file, f"{gst_number}/{file_name}")
                    setattr(gst_instance, f"{field_name}_url", url)

            gst_instance.save()

            request.session['gst_number'] = gst_number
            return redirect('success_page')
        else:
            print("Form Errors:", form.errors.as_json())
    else:
        form = GSTForm()

    return render(request, 'form.html', {'form': form})


@api_view(['POST'])
def submit_gst_form(request):
    print("Incoming Data:", request.data)
    serializer = GSTDeclarationSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response({
            "success": True,
            "gst_number": instance.gst_number
        })
    else:
        print("Serializer Errors:", serializer.errors)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


def success_page(request):
    gst_number = request.session.get('gst_number')
    return render(request, 'success.html', {'gst_number': gst_number})

# API to Get GST Details by GST Number
@api_view(['GET'])
def get_gst_details(request, gst_number):
    try:
        gst_data = GSTDeclaration.objects.get(gst_number=gst_number)
        serializer = GSTDeclarationSerializer(gst_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except GSTDeclaration.DoesNotExist:
        return Response({"error": "GST details not found"}, status=status.HTTP_404_NOT_FOUND)

def form_view(request):
    return render(request, 'form.html')


def upload_file_to_s3(file, filename, gst_number):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)

    bucket = settings.AWS_STORAGE_BUCKET_NAME
    key = f"{gst_number}/{filename}"  # Folder = GST number
    s3.upload_fileobj(file, bucket, key)
    url = f"https://{bucket}.s3.amazonaws.com/{key}"
    return url


from .models import GSTDeclaration

def fetch_image_urls(gst_number):
    try:
        data = GSTDeclaration.objects.get(gst_number=gst_number)
        return {
            "customer_photo": data.customer_photo_url,
            "gst_certification_photo": data.gst_certification_photo_url,
            "udyan_photo_url": data.udyan_adhar_photo_url,
            "personal_pan_photo": data.personal_pan_photo_url,
            "personal_adhar_photo": data.personal_adhar_photo_url,
            "drug_license_photo20b": data.drug_license_photo_url20b,
            "drug_license_photo21b": data.drug_license_photo_url21b,
            "drug_license_photo20d": data.drug_license_photo_url20d,
            "food_license_photo": data.food_license_photo_url,
            "shop_photo": data.shop_photo_url,
        }
    except GSTDeclaration.DoesNotExist:
        return None

# def generate_acknowledgement_pdf(request, gst_number):
#     instance = GSTDeclaration.objects.filter(gst_number=gst_number).first()
#     if not instance:
#         return HttpResponse("Invalid GST Number", status=404)

#     context = {
#         'financial_year': instance.year_of_filing,
#         'gst_number': instance.gst_number,
#         'pan_number': instance.pan_number,
#         'tan_number': instance.tan_number or "N/A",
#         'company_name': instance.company_name,
#         'city': instance.city,
#         'year_of_filing': instance.year_of_filing,
#         'current_date': datetime.date.today().strftime("%d-%m-%Y"),
#         'current_time': datetime.datetime.now().strftime("%I:%M %p"),
#         'turnover': instance.turnover ,
#         'tds_tcs': "tds" if instance.turnover == "yes" else "tcs",
#     }

#     html_string = render_to_string('pdf_template.html', context)
#     result = BytesIO()
    
#     pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), dest=result)
    
#     if pdf.err:
#         return HttpResponse("PDF generation failed", status=500)

#     # Save a copy of the PDF data
#     pdf_bytes = result.getvalue()

#     # Upload using a new BytesIO stream
#     s3_filename = f"gst/acknowledgment/acknowledgement_{gst_number}_{instance.year_of_filing}.pdf"
#     # upload_file_to_s3(BytesIO(pdf_bytes), s3_filename, gst_number)
#     default_storage.save(s3_filename, ContentFile(result.getvalue()))
    
#     # Send PDF as HTTP response
#     response = HttpResponse(pdf_bytes, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=acknowledgement_{gst_number}_{instance.year_of_filing}.pdf'
#     return response

def generate_acknowledgement_pdf(request, gst_number):
    instance = GSTDeclaration.objects.filter(gst_number=gst_number).first()
    if not instance:
        return HttpResponse("Invalid GST Number", status=404)

    context = {
        'financial_year': instance.year_of_filing,
        'gst_number': instance.gst_number,
        'pan_number': instance.pan_number,
        'tan_number': instance.tan_number or "N/A",
        'company_name': instance.company_name,
        'city': instance.city,
        'year_of_filing': instance.year_of_filing,
        'current_date': datetime.date.today().strftime("%d-%m-%Y"),
        'current_time': datetime.datetime.now().strftime("%I:%M %p"),
        'turnover': instance.turnover,
        'tds_tcs': "tds" if instance.turnover == "yes" else "tcs", 
    }

    html_string = render_to_string('pdf_template.html', context)
    result = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), dest=result)
    
    if pdf.err:
        return HttpResponse("PDF generation failed", status=500)

    # Save a copy of the PDF data
    pdf_bytes = result.getvalue()

    #changes were here
    # Upload using a new BytesIO stream
    s3_filename = f"gst/acknowledgment/acknowledgement_{gst_number}_{instance.year_of_filing}.pdf"
    default_storage.save(s3_filename, ContentFile(result.getvalue()))

    # Build full URL to the uploaded file
    s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/{s3_filename}"

    # Save the URL to the instance and persist it
    instance.acknowledgement_pdf_url = s3_url
    instance.save()

    # Send PDF as HTTP response
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=acknowledgement_{gst_number}_{instance.year_of_filing}.pdf'
    return response


def upload_documents(request):
    return render(request, 'upload_documents.html')

def verify_gst(request):
    if request.method == 'POST':
        gst_number = request.POST.get('gst_number')

        try:
            gst_entry = GSTDeclaration.objects.get(gst_number=gst_number)

            # Store GST number in session for later use
            request.session['gst_number'] = gst_number

            # GST exists
            return render(request, 'gst_verified.html', {
                'gst_number': gst_number,
                'message': 'GST Number Verified ✅',
                'next_url': 'document_form'
            })
        except GSTDeclaration.DoesNotExist:
            # GST does not exist
            return render(request, 'gst_not_found.html', {
                'gst_number': gst_number,
                'message': 'GST Number Not Found ❌',
                'register_url': 'gst_form_view'  # use {% url 'gst_form_view' %} in template
            })

    return redirect('upload_documents')



def generate_updated_pdf(request, gst_number):
    try:
        instance = GSTDeclaration.objects.get(gst_number=gst_number)
        
        # Prepare context using already saved data
        context = {
            'gst_number': instance.gst_number,
            'company_name': instance.company_name,
            'year_of_filing': instance.year_of_filing,
            'tds_tcs': 'TDS' if instance.tds_tcs == 'tds' else 'TCS',
            'current_date': datetime.date.today().strftime("%d-%m-%Y"),
            'financial_year': instance.year_of_filing,
            'pan_number': instance.pan_number,
            'tan_number': instance.tan_number or "N/A",
            'city': instance.city,
            'current_time': datetime.datetime.now().strftime("%I:%M %p"),
            'turnover': instance.turnover  
        }

        # Generate PDF
        html_string = render_to_string('pdf_template.html', context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        
        if pdf.err:
            return HttpResponse("PDF generation failed", status=500)

        # Upload to S3
        pdf_bytes = result.getvalue()
        s3_filename = f"gst/acknowledgment/acknowledgement_{gst_number}_updated_{instance.year_of_filing}.pdf"
    # upload_file_to_s3(BytesIO(pdf_bytes), s3_filename, gst_number)
        default_storage.save(s3_filename, ContentFile(result.getvalue()))

        # Build full URL to the uploaded file
        s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/{s3_filename}"
        
        # Save the URL to the instance and persist it
        instance.acknowledgement_pdf_url = s3_url
        instance.save()

        # Return PDF response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="acknowledgement_{gst_number}_updated_{instance.year_of_filing}.pdf"'
        return response

    except GSTDeclaration.DoesNotExist:
        return HttpResponse("GST record not found", status=404)
    except Exception as e:
        return HttpResponse(f"PDF generation error: {str(e)}", status=500)
    return response

def document_form(request):
    gst_number = request.session.get('gst_number')
    if not gst_number:
        return HttpResponse("Session expired", status=400)

    if request.method == 'POST':
        try:
            # Get form data
            year_of_filing = request.POST.get("year_of_filing")
            turnover = request.POST.get("turnover")  # 'yes' or 'no'
            tds_tcs = 'tds' if turnover == 'yes' else 'tcs'


            if not year_of_filing or not turnover:
                return HttpResponse("Missing required fields", status=400)

            # Get or create GST declaration
            instance, created = GSTDeclaration.objects.get_or_create(
                gst_number=gst_number,
                defaults={
                    'year_of_filing': year_of_filing,
                    'turnover': turnover,
                    'tds_tcs' : tds_tcs,
                }
            )

            # Update existing record if not created
            if not created:
                instance.year_of_filing = year_of_filing
                instance.turnover = turnover
                instance.tds_tcs = 'tds' if turnover == 'yes' else 'tcs'
                instance.save()

            # Generate and return PDF
            return generate_updated_pdf(request, gst_number)
            
        except Exception as e:
            return HttpResponse(f"Error processing request: {str(e)}", status=500)
        

    # GET request - show form
    return render(request, 'document_form.html', {'gst_number': gst_number})

def success_end(request):
    gst_number = request.GET.get('gst_number')
    if not gst_number:
        return HttpResponse("GST number missing", status=400)
    
    return render(request, 'success_end.html', {
        'gst_number': gst_number,
        'current_date': datetime.datetime.now().strftime("%d-%m-%Y"),
        'current_time': datetime.datetime.now().strftime("%I:%M %p"),
    })
    
def back_to_home(request):
    return render(request, 'home.html')
