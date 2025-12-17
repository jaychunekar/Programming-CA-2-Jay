import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import random

print("="*80)
print("Hotel Room Price Data Extraction System")
print("="*80)

# Define the HTML files to scrape
html_files = ['seaside_paradise.html', 'mountain_view_lodge.html']

# Define date range
start_date = datetime(2025, 12, 20)
end_date = datetime(2025, 12, 30)

print(f"\nDate Range: {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}")
print(f"Duration: {(end_date - start_date).days + 1} days")

# List to store all scraped data
all_hotel_data = []

# Loop through each HTML file
for html_file in html_files:
    print("\n" + "-"*80)
    print(f"Processing: {html_file}")
    print("-"*80)
    
    try:
        # Read the HTML file
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        print(f"Successfully read {html_file}")
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find hotel name
        hotel_name_tag = soup.find('h1', class_='hotel-name')
        hotel_name = hotel_name_tag.get('data-hotel-name')
        print(f"Hotel Name: {hotel_name}")
        
        # Find hotel location
        location_tag = soup.find('p', class_='hotel-location')
        location = location_tag.get('data-location')
        print(f"Location: {location}")
        
        # Find all room cards
        room_cards = soup.find_all('div', class_='room-card')
        print(f"Found {len(room_cards)} rooms")
        
        # Process each room
        for card in room_cards:
            # Extract room type
            room_type_tag = card.find('h2', class_='room-type')
            room_type = room_type_tag.get('data-room-type')
            
            # Extract price
            price_tag = card.find('div', class_='price')
            base_price = float(price_tag.get('data-price'))
            currency = price_tag.get('data-currency')
            
            # Extract amenities
            amenities_tag = card.find('p', class_='amenities')
            amenities = amenities_tag.get('data-amenities')
            
            # Extract capacity
            capacity_tag = card.find('span', class_='capacity')
            capacity = capacity_tag.get('data-capacity')
            
            # Extract availability
            availability_tag = card.find('span', class_='availability')
            availability = availability_tag.get('data-availability')
            
            print(f"  - {room_type}: €{base_price}")
            
            # Generate price for each date in range
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                day_name = current_date.strftime("%A")
                
                # Calculate price with weekend and holiday premiums
                final_price = base_price
                
                # Weekend pricing (Friday & Saturday)
                if day_name in ['Friday', 'Saturday']:
                    final_price = final_price * 1.25
                
                # Holiday pricing (24-26 Dec, 31 Dec)
                if current_date.day in [24, 25, 26, 31]:
                    final_price = final_price * 1.40
                
                # Add random variation
                variation = random.uniform(0.95, 1.05)
                final_price = round(final_price * variation, 2)
                
                # Store data
                record = {
                    'Date': date_str,
                    'Day': day_name,
                    'Hotel_Name': hotel_name,
                    'Location': location,
                    'Room_Type': room_type,
                    'Base_Price': base_price,
                    'Final_Price': final_price,
                    'Currency': currency,
                    'Amenities': amenities,
                    'Max_Capacity': capacity,
                    'Availability': availability
                }
                
                all_hotel_data.append(record)
                
                current_date += timedelta(days=1)
        
        print(f"Completed scraping {html_file}")
        
    except FileNotFoundError:
        print(f"Error: File {html_file} not found!")
    except Exception as e:
        print(f"Error processing {html_file}: {str(e)}")

print("\n" + "="*80)
print(f"Total records collected: {len(all_hotel_data)}")
print("="*80)

# Save to CSV file
csv_filename = "hotel_data.csv"

print(f"\nSaving data to {csv_filename}...")

try:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define field names
        fieldnames = ['Date', 'Day', 'Hotel_Name', 'Location', 'Room_Type', 
                     'Base_Price', 'Final_Price', 'Currency', 'Amenities', 
                     'Max_Capacity', 'Availability']
        
        # Create CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write all rows
        writer.writerows(all_hotel_data)
    
    print(f"Successfully saved {len(all_hotel_data)} records to {csv_filename}")

except Exception as e:
    print(f"Error saving CSV: {str(e)}")

print("\n" + "="*80)
print("Reading and displaying data from CSV file...")
print("="*80)

# Read from CSV and display
try:
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_from_csv = list(reader)
    
    print(f"\nSuccessfully read {len(data_from_csv)} records from CSV")
    
    # Display data in terminal
    print("\n" + "="*100)
    print("HOTEL ROOM PRICING DATA")
    print("="*100)
    
    # Group by hotel
    hotels = {}
    for row in data_from_csv:
        hotel = row['Hotel_Name']
        if hotel not in hotels:
            hotels[hotel] = []
        hotels[hotel].append(row)
    
    # Display each hotel's data
    for hotel_name, hotel_records in hotels.items():
        print(f"\n{'─'*100}")
        print(f"Hotel: {hotel_name}")
        print(f"Location: {hotel_records[0]['Location']}")
        print(f"{'─'*100}")
        
        # Get unique rooms
        rooms = {}
        for record in hotel_records:
            room_type = record['Room_Type']
            if room_type not in rooms:
                rooms[room_type] = []
            rooms[room_type].append(record)
        
        # Display each room type
        for room_type, room_records in rooms.items():
            sample = room_records[0]
            print(f"\nRoom Type: {room_type}")
            print(f"  Base Price: €{sample['Base_Price']}")
            print(f"  Capacity: {sample['Max_Capacity']} persons")
            print(f"  Amenities: {sample['Amenities']}")
            print(f"  Availability: {sample['Availability']}")
            print(f"\n  Sample Dates and Prices:")
            print(f"  {'Date':<12} {'Day':<10} {'Price':<10}")
            print(f"  {'-'*35}")
            
            # Show first 5 dates
            for i, record in enumerate(room_records[:5]):
                print(f"  {record['Date']:<12} {record['Day']:<10} €{record['Final_Price']:<10}")
            
            if len(room_records) > 5:
                print(f"  ... and {len(room_records) - 5} more dates")
    
    # Display statistics
    print(f"\n\n{'='*100}")
    print("SUMMARY STATISTICS")
    print(f"{'='*100}")
    
    # Calculate statistics
    all_prices = [float(row['Final_Price']) for row in data_from_csv]
    
    print(f"\nTotal Records: {len(data_from_csv)}")
    print(f"Number of Hotels: {len(hotels)}")
    print(f"Total Room Types: {sum(len(set(r['Room_Type'] for r in records)) for records in hotels.values())}")
    print(f"\nPrice Statistics:")
    print(f"  Minimum Price: €{min(all_prices):.2f}")
    print(f"  Maximum Price: €{max(all_prices):.2f}")
    print(f"  Average Price: €{sum(all_prices)/len(all_prices):.2f}")
    
    # Average price per hotel
    print(f"\nAverage Price by Hotel:")
    for hotel_name, hotel_records in hotels.items():
        hotel_prices = [float(r['Final_Price']) for r in hotel_records]
        avg_price = sum(hotel_prices) / len(hotel_prices)
        print(f"  {hotel_name}: €{avg_price:.2f}")
    
    print("\n" + "="*100)
    print("Process completed successfully!")
    print("="*100)

except FileNotFoundError:
    print(f"Error: CSV file {csv_filename} not found!")
except Exception as e:
    print(f"Error reading CSV: {str(e)}")