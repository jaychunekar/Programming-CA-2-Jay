import os
import PyPDF2
import pdfplumber
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
import requests
from django.conf import settings

# Optional: pytesseract for OCR (requires Tesseract OCR to be installed)
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False


def extract_pdf_data(file_path):
    """Extract text data from PDF file"""
    text_data = []
    
    try:
        # Try using pdfplumber first (better for tables)
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_data.append({
                        'page': page.page_number,
                        'text': text
                    })
    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_data.append({
                            'page': page_num,
                            'text': text
                        })
        except Exception as e2:
            print(f"Error with PyPDF2: {e2}")
    
    return {
        'type': 'pdf',
        'pages': len(text_data),
        'content': text_data
    }


def extract_excel_data(file_path):
    """Extract data from Excel file"""
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        sheets_data = {}
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Convert DataFrame to dictionary
            sheets_data[sheet_name] = {
                'columns': df.columns.tolist(),
                'rows': df.values.tolist(),
                'row_count': len(df)
            }
        
        return {
            'type': 'excel',
            'sheets': sheets_data
        }
    except Exception as e:
        print(f"Error extracting Excel data: {e}")
        return {
            'type': 'excel',
            'error': str(e)
        }


def extract_image_data(file_path):
    """Extract text from image using OCR"""
    try:
        # Note: pytesseract requires Tesseract OCR to be installed
        # For production, you might want to use a cloud OCR service
        image = Image.open(file_path)
        
        # Try OCR if pytesseract is available and configured
        if PYTESSERACT_AVAILABLE:
            try:
                text = pytesseract.image_to_string(image)
                return {
                    'type': 'image',
                    'text': text,
                    'format': image.format,
                    'size': image.size
                }
            except Exception:
                # If OCR fails, return image metadata
                return {
                    'type': 'image',
                    'format': image.format,
                    'size': image.size,
                    'mode': image.mode,
                    'note': 'OCR not available. Install Tesseract OCR for text extraction.'
                }
        else:
            # If pytesseract is not installed, return image metadata
            return {
                'type': 'image',
                'format': image.format,
                'size': image.size,
                'mode': image.mode,
                'note': 'OCR not available. Install pytesseract and Tesseract OCR for text extraction.'
            }
    except Exception as e:
        print(f"Error extracting image data: {e}")
        return {
            'type': 'image',
            'error': str(e)
        }


def scrape_website(url):
    """Scrape data from website using BeautifulSoup"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract various elements
        data = {
            'type': 'website',
            'url': url,
            'title': soup.title.string if soup.title else None,
            'headings': {
                'h1': [h.get_text().strip() for h in soup.find_all('h1')],
                'h2': [h.get_text().strip() for h in soup.find_all('h2')],
                'h3': [h.get_text().strip() for h in soup.find_all('h3')],
            },
            'paragraphs': [p.get_text().strip() for p in soup.find_all('p')],
            'links': [{'text': a.get_text().strip(), 'href': a.get('href')} for a in soup.find_all('a', href=True)],
            'images': [{'alt': img.get('alt', ''), 'src': img.get('src')} for img in soup.find_all('img', src=True)],
            'meta_description': soup.find('meta', attrs={'name': 'description'}),
            'text_content': soup.get_text()[:5000]  # First 5000 characters
        }
        
        # Clean up meta description
        if data['meta_description']:
            data['meta_description'] = data['meta_description'].get('content', '')
        
        return data
    except requests.exceptions.RequestException as e:
        return {
            'type': 'website',
            'url': url,
            'error': f'Failed to fetch website: {str(e)}'
        }
    except Exception as e:
        return {
            'type': 'website',
            'url': url,
            'error': f'Error scraping website: {str(e)}'
        }

