# Data Capture System

A Django-based web application for capturing and storing data from various sources including PDFs, Excel files, images, and websites. The system uses MongoDB for data storage and JWT for authentication.

## Features

- 🔐 **JWT Authentication**: Secure user authentication using JSON Web Tokens
- 📄 **PDF Processing**: Extract text data from PDF files
- 📊 **Excel Processing**: Extract data from Excel files (.xlsx, .xls)
- 🖼️ **Image Processing**: Extract text from images using OCR (requires Tesseract)
- 🌐 **Web Scraping**: Scrape data from websites using BeautifulSoup
- 💾 **MongoDB Storage**: Store extracted data in MongoDB
- 🎨 **Bootstrap UI**: Modern, responsive user interface
- 🔒 **Protected Routes**: Home page requires authentication

## Prerequisites

- Python 3.8 or higher
- MongoDB (running locally or remote)
- pip (Python package manager)

### Optional (for Image OCR)
- Tesseract OCR installed on your system
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "Scrap Project"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up MongoDB**
   - Make sure MongoDB is running on your system
   - Default connection: `mongodb://localhost:27017/`
   - You can set custom MongoDB connection using environment variable:
     ```bash
     set MONGODB_HOST=mongodb://your-mongodb-host:27017/
     ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - You'll be redirected to the login page

## Usage

### User Registration
1. Click on "Register" in the navigation bar
2. Fill in your username, email, and password
3. Click "Register"
4. You'll be redirected to the login page

### User Login
1. Enter your username and password
2. Click "Login"
3. You'll be redirected to the home page

### Upload Files
1. On the home page, select a file (PDF, Excel, or Image)
2. Choose the file type from the dropdown
3. Click "Upload & Extract Data"
4. The extracted data will be stored in MongoDB

### Scrape Websites
1. On the home page, enter a website URL
2. Click "Scrape Website"
3. The scraped data will be extracted and stored in MongoDB

### View Recent Sources
- The home page displays your recent data sources
- Each source shows the type, name/URL, creation date, and status

## Project Structure

```
scrap_project/
├── authentication/          # User authentication app
│   ├── models.py           # User model
│   ├── views.py            # Authentication views
│   └── urls.py             # Authentication URLs
├── data_capture/           # Data capture app
│   ├── models.py           # DataSource model
│   ├── views.py            # File upload and scraping views
│   ├── utils.py            # Data extraction utilities
│   └── urls.py             # Data capture URLs
├── scrap_project/          # Main project settings
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL configuration
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── authentication/     # Login/Register templates
│   └── data_capture/       # Home page template
├── media/                  # Uploaded files (created automatically)
├── static/                 # Static files (CSS, JS)
├── requirements.txt        # Python dependencies
└── manage.py               # Django management script
```

## API Endpoints

### Authentication
- `POST /api/auth/api/register/` - Register a new user
- `POST /api/auth/api/login/` - Login and get JWT tokens
- `POST /api/auth/api/logout/` - Logout (blacklist token)

### Data Capture
- `POST /api/data/api/upload/` - Upload and process a file (requires authentication)
- `POST /api/data/api/scrape/` - Scrape a website (requires authentication)

## Configuration

### MongoDB Connection
Set the `MONGODB_HOST` environment variable to change the MongoDB connection:
```bash
set MONGODB_HOST=mongodb://your-host:27017/
```

### File Upload Limits
Default maximum file size is 10MB. You can change this in `scrap_project/settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
```

## Troubleshooting

### MongoDB Connection Error
If you see MongoDB connection errors:
1. Make sure MongoDB is running
2. Check the connection string in settings.py
3. You can temporarily use SQLite by uncommenting the SQLite database configuration in settings.py

### Image OCR Not Working
If image text extraction doesn't work:
1. Install Tesseract OCR on your system
2. The system will still upload images but won't extract text without Tesseract

### Import Errors
If you encounter import errors:
1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Make sure your virtual environment is activated

## Security Notes

- Change the `SECRET_KEY` in `settings.py` before deploying to production
- Set `DEBUG = False` in production
- Configure proper `ALLOWED_HOSTS` for production
- Use environment variables for sensitive configuration
- Consider using HTTPS in production

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the Django documentation or MongoDB documentation.


