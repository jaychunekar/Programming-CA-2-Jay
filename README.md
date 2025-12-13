# Advanced Programming Techniques - CA_ONE

**Student ID**: 20068781  
**Name**: Jay Chunekar  
**Course**: MSc Cyber Security  
**Module**: B9CY108  

## Project Structure

### Question 1: Contact Book Management System (C#)
- `Program.cs` - Contact book application with CRUD operations
- `ContactBookApp.csproj` - Project file
- `screenshots/` - Screenshots showing working application

### Question 2: File Extension Information System (C#)
- `Program.cs` - File extension lookup system
- `FileExtensionApp.csproj` - Project file
- `screenshots/` - Screenshots showing working application

### Question 3: Client-Server Application (Python)
- `Que3_server.py` - Server application for DBS admissions
- `Que3_client.py` - Client application for student applications
- `dbs_applications.db` - SQLite database storing applications
- `screenshots/` - Screenshots showing working application

### Question 4: Hotel Data Extraction System (Python)
- `Que4.py` - Web scraping application for hotel data
- `seaside_paradise.html` - Sample hotel 1 webpage
- `mountain_view_lodge.html` - Sample hotel 2 webpage
- `hotel_data.csv` - Generated CSV with extracted data
- `screenshots/` - Screenshots showing working application

## How to Run

### Question 1 - Contact Book Management System
**Using Visual Studio**
```bash
Open ContactBookApp.sln and press F5 to run
```
**Using Command Line**
```bash
cd Question1_ContactBook
dotnet run
```

### Question 2 - File Extension Information System
**Using Visual Studio**
```bash
Open FileExtensionApp.sln and press F5 to run
```
**Using Command Line**
```bash
cd Question2_FileExtension
dotnet run
```

### Question 3 - Client-Server Application
**Step 1: Start the Server**
```bash
python Que3_server.py
```
**Step 2: Run the Client (in new terminal)**
```bash
python Que3_client.py
```

### Question 4 - Hotel Data Extraction System
```bash
python Que4.py
```

## Requirements

### C# Projects (Question 1 & 2)
- .NET SDK 6.0 or higher
- Visual Studio 2022 or VS Code (optional)

### Python Projects (Question 3 & 4)
- Python 3.10 or higher
- Built-in modules: socket, sqlite3, json, uuid, csv, datetime
- External module: beautifulsoup4

**Install Python dependencies:**
```bash
pip install beautifulsoup4
```

## Key Features

### Question 1
- 20 pre-populated contacts
- CRUD operations (Create, Read, Update, Delete)
- Mobile number validation (9 digits)
- Method overloading demonstration
- Object-oriented programming principles

### Question 2
- 25+ file extensions database
- Dictionary-based fast lookup
- Category-based browsing
- Graceful error handling for unknown extensions

### Question 3
- TCP connection-oriented protocol
- SQLite database for persistent storage
- UUID-based unique application numbers
- Input validation with retry mechanism

### Question 4
- HTML parsing using BeautifulSoup
- Dynamic pricing with weekend/holiday premiums
- CSV data export
- Statistical analysis (min, max, average prices)

## Submission Date
December 13, 2025
