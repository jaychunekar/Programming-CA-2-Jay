from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import DataSource, ExtractedData
from .utils import extract_pdf_data, extract_excel_data, extract_image_data, scrape_website
import os
import json


@login_required
def home(request):
    """Home page view - requires login"""
    user_sources = DataSource.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'data_capture/home.html', {
        'sources': user_sources
    })


@login_required
def upload_file(request):
    """Handle file upload"""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        source_type = request.POST.get('source_type', 'other')
        
        if not uploaded_file:
            messages.error(request, 'Please select a file')
            return redirect('home')
        
        # Create media directory if it doesn't exist
        media_dir = settings.MEDIA_ROOT / 'uploads'
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded file
        file_path = media_dir / uploaded_file.name
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Extract data based on file type
        extracted_data = None
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == '.pdf' or source_type == 'pdf':
            extracted_data = extract_pdf_data(str(file_path))
        elif file_extension in ['.xlsx', '.xls'] or source_type == 'excel':
            extracted_data = extract_excel_data(str(file_path))
        elif file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp'] or source_type == 'image':
            extracted_data = extract_image_data(str(file_path))
        else:
            messages.warning(request, f'File type {file_extension} not fully supported')
            extracted_data = {
                'type': 'other',
                'file_name': uploaded_file.name,
                'message': 'File uploaded but extraction not implemented for this type'
            }
        
        # Create DataSource record
        data_source = DataSource.objects.create(
            user=request.user,
            source_type=source_type if source_type != 'other' else file_extension[1:],
            file_name=uploaded_file.name
        )
        
        # Save to MongoDB
        if extracted_data:
            ExtractedData.objects.create(
        source=data_source,
        user=request.user,
        data=json.dumps(extracted_data, default=str),
    )
            messages.success(request, 'File uploaded and data extracted successfully!')
        else:
            messages.error(request, 'Failed to extract data from file')
        
        return redirect('home')
    
    return redirect('home')


@login_required
def scrape_url(request):
    """Handle website URL scraping"""
    if request.method == 'POST':
        url = request.POST.get('url')
        
        if not url:
            messages.error(request, 'Please provide a URL')
            return redirect('home')
        
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Scrape the website
        extracted_data = scrape_website(url)
        
        # Create DataSource record
        data_source = DataSource.objects.create(
            user=request.user,
            source_type='website',
            website_url=url
        )
        
        # Save to MongoDB
        if extracted_data and 'error' not in extracted_data:
            ExtractedData.objects.create(
        source=data_source,
        user=request.user,
        data=json.dumps(extracted_data, default=str),
    )
            messages.success(request, 'Website scraped successfully!')
        else:
            error_msg = extracted_data.get('error', 'Unknown error') if isinstance(extracted_data, dict) else 'Failed to scrape website'
            messages.error(request, f'Error scraping website: {error_msg}')
        
        return redirect('home')
    
    return redirect('home')


@login_required
@csrf_exempt
def api_upload_file(request):
    """API endpoint for file upload"""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        source_type = request.POST.get('source_type', 'other')
        
        if not uploaded_file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        # Create media directory if it doesn't exist
        media_dir = settings.MEDIA_ROOT / 'uploads'
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded file
        file_path = media_dir / uploaded_file.name
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Extract data based on file type
        extracted_data = None
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == '.pdf' or source_type == 'pdf':
            extracted_data = extract_pdf_data(str(file_path))
        elif file_extension in ['.xlsx', '.xls'] or source_type == 'excel':
            extracted_data = extract_excel_data(str(file_path))
        elif file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp'] or source_type == 'image':
            extracted_data = extract_image_data(str(file_path))
        else:
            extracted_data = {
                'type': 'other',
                'file_name': uploaded_file.name,
                'message': 'File uploaded but extraction not implemented for this type'
            }
        
        # Create DataSource record
        data_source = DataSource.objects.create(
            user=request.user,
            source_type=source_type if source_type != 'other' else file_extension[1:],
            file_name=uploaded_file.name
        )
        
        # Save to MongoDB
        if extracted_data:
            ExtractedData.objects.create(
        source=data_source,
        user=request.user,
        data=json.dumps(extracted_data, default=str),
    )
            return JsonResponse({
                'message': 'File uploaded and processed successfully',
                'source_id': data_source.id,
                'data': extracted_data
            })
        else:
            return JsonResponse({'error': 'Failed to extract data'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def api_scrape_url(request):
    """API endpoint for URL scraping"""
    if request.method == 'POST':
        url = request.POST.get('url') or request.data.get('url')
        
        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)
        
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Scrape the website
        extracted_data = scrape_website(url)
        
        # Create DataSource record
        data_source = DataSource.objects.create(
            user=request.user,
            source_type='website',
            website_url=url
        )
        
        # Save to MongoDB
        if extracted_data and 'error' not in extracted_data:
            ExtractedData.objects.create(
        source=data_source,
        user=request.user,
        data=json.dumps(extracted_data, default=str),
    )
            return JsonResponse({
                'message': 'Website scraped successfully',
                'source_id': data_source.id,
                'data': extracted_data
            })
        else:
            error_msg = extracted_data.get('error', 'Unknown error') if isinstance(extracted_data, dict) else 'Failed to scrape'
            return JsonResponse({'error': error_msg}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


