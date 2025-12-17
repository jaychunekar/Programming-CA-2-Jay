#Que3_client.py
#This is the client that students use to apply

#Importing necessary modules
import socket               #For network communication      
import json                 #To format the data which is being sent


#Step 1: Function to get User Input

def get_application_details():     #It collects all the required information from the applicant
    
    print("\n" + "=" *60)
    print("DUBLIN BUSINESS SCHOOL - APPLICATION FORM")
    print("=" * 60)


    #To get name
    while True:
        name = input("\n Enter your full name: ").strip()
        if name and len(name) >= 2:
            break
        print("Please enter a valid name (at least 2 characters)")

    #To get address
    while True:
        address = input("Enter your address: ").strip()
        if address and len(address) >= 5:
            break
        print("Please enter a valid address (at least 5 characters)")

    #To get educational qualifications
    while True:
        qualifications = input("Enter your educational qualifications: ").strip()
        if qualifications and len(qualifications) >= 3:
            break
        print("Please enter your qualifications (at least 3 characters)")

    #To get course selection
    print("\nAvailable Courses:")
    print("1. MSc in Cyber Security")
    print("2. Msc in Information Systems & Computing")
    print("3. Msc in Data Analytics")

    courses = {
        '1' : 'Msc in Cyber Security',
        '2' : 'Msc in Information Systems & Computing',
        '3' : 'Msc in Data Analytics'
    }

    while True:
        course_choice = input("\nSelect course (1-3):") .strip()
        if course_choice in courses:
            course = courses[course_choice]
            break
        print("Please select a valid option (1, 2 or 3)")
                              
    #Get start year
    while True:
        try:
            start_year = int(input("Enter intended start year: "). strip())
            if 2024 <= start_year <= 2030:
                break
            print("Please enter a year between 2024 and 2030")
        except ValueError:
            print("Please enter a valid year (numbers only)")

    #Get start month
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ]

    print("\nAvailable Months: ")
    for i, month in enumerate(months, 1):
        print(f"{i:2d}.{month}")

    while True:
        try:
            month_choice = int(input("\nSelect start month (1-12):").strip())
            if 1 <= month_choice <= 12:
                start_month = months[month_choice - 1]
                break
            print("Please enter a number between 1 and 12")
        except ValueError:
            print("Please enter a valid number")


    #Create dictionary with all data
    application_data = {
        'name': name,
        'address': address,
        'qualifications': qualifications,
        'course': course,
        'start_year': start_year,
        'start_month': start_month
    }

    return application_data

#Step 2: The function to send the apliocation to the server

def send_application(application_data):      #It connects to the server and sends application data

    #Server details It must always match the the server settings
    HOST = '127.0.0.1'  #localhost
    PORT = 65432        #Same port as server

    try:
        #Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("\n[CLIENT] Connecting to DBS Server...")

        #Connecting to server
        client_socket.connect((HOST, PORT))
        print("[CLIENT] Connected to server successfully..!")

        #Convert dictionary to JSON string
        data_to_send = json.dumps(application_data)

        #Send data to server
        client_socket.send(data_to_send.encode('utf-8'))
        print("[CLIENT] Application data sent to server")

        #Waiting for the response from server
        print("[CLIENT] Waitinf for the response...")
        response = client_socket.recv(4096).decode('utf-8')

        #Convert JSON response back to dictionary
        response_data = json.loads(response)

        #Display the response
        print("\n" + "=" * 60)
        if response_data['status'] == 'success':
            print("APPLICATION SUBMITTED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\n Your Application Number: {response_data['application_number']}")
            print("Please save this number for future reference.")
            print("You will receive further communication from DBS soon...")
        else:
            print("Application Failed...")
            print("=" * 60)
            print(f"\n Error: {response_data['message']}")

        print("=" * 60)

        #Close the connection
        client_socket.close()
        print("\n[CLIENT] Connection closed")

        return True
    
    except ConnectionRefusedError:
        print("\n ERROR: Cannot connect to server")
        print("Make sure the server is running first!")
        return False
    
    except Exception as e:
        print(f"\n Error: {e}")
        return False
    
#Step 3: Main Program

def main():              #Main function that runs the client application
     print("\n" + "🎓" * 30)
     print(" WELCOME TO DUBLIN BUSINESS SCHOOL")
     print(" Online Application System")
     print("🎓" * 30)

     while True:
         print("\n" + "-" * 60)
         choice = input("\nWould you like to submit an application? (yes/no): ").strip().lower()

         if choice in ['yes', 'y']:
             #Getting the application details
             app_data = get_application_details()

             #Showing summary and confirming
             print("\n" + "-" * 60)
             print("APPLICATION SUMMARY")
             print("-" * 60)
             print(f" Name:              {app_data['name']}")
             print(f" Address:           {app_data['address']}")
             print(f" Qualifications:    {app_data['qualifications']}")
             print(f" Course:            {app_data['course']}")
             print(f" Start:             {app_data['start_month']} {app_data['start_year']}")
             print("-" * 60)

             confirm = input("\nConfirm Submission? (yes/no): ").strip().lower()

             if confirm in ['yes', 'y']:
                 #Send to server
                 send_application(app_data)
             else:
                 print("Application cancelled...")

         elif choice in ['no', 'n']:
             print("\n Thank you for visiting DBS Application System!")
             print("Goodbye..!!\n")
             break
         
         else:
             print("Please enter 'yes' or 'no'")

#Running the client

if __name__ == "__main__":
    main()
             


