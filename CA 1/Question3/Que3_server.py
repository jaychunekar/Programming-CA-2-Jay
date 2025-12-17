#Ques3_server.py
#This is the server that receives the student applications

#First I will import necessary modules
import socket                               #This is for network communication
import sqlite3                              #This is for database operations
import uuid                                 #This is for generating unique ids
import json                                 #This is to format data which will be sent or received

#Step 1: Let's start with creating the database
print("[DEBUG] Running server file:", __file__)
def create_database():                      #By writing this function a database and table will be created if they do not exist

    connection = sqlite3.connect('dbs_applications.db')  #It connects to database and creates a file if it doesn't exist
    cursor = connection.cursor()


    #Creating table for storing the muliple applications
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS applications(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            application_number TEXT UNIQUE NOT NULL,
                            name TEXT NOT NULL,
                            address TEXT NOT NULL,
                            qualifications TEXT NOT NULL,
                            course TEXT NOT NULL,
                            start_year INTEGER NOT NULL,
                            start_month TEXT NOT NULL,
                            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    ''')
    

    connection.commit()                     #To save changes
    connection.close()                      #TO close the connection
    print("[DATABASE] Database and table created successfully")
    

#Step 2: Let's start with generating unique application numbers

def generate_application_number():        #Generates a unique application number

    unique_id = str(uuid.uuid4())[:8].upper()   #It will get the first 8 characters of UUID
    app_number = f"APP-{unique_id}"
    return app_number
    

#Step 3: Save Application to Database

def save_application(data):  # It saves the student's application to the database and returns the application number
    connection = sqlite3.connect('dbs_applications.db')
    cursor = connection.cursor()

    # Generate unique application number
    app_number = generate_application_number()

    sql = (
        "INSERT INTO applications ("
        "application_number, name, address, qualifications, course, start_year, start_month"
        ") VALUES (?, ?, ?, ?, ?, ?, ?)"
    )

    try:
        cursor.execute(sql, (
            app_number,
            data['name'],
            data['address'],
            data['qualifications'],
            data['course'],
            data['start_year'],
            data['start_month']
        ))

        connection.commit()
        print(f"[DATABASE] Application saved with number: {app_number}")
        return app_number

    except sqlite3.IntegrityError as e:
        print("[DATABASE] IntegrityError (duplicate app number):", e)
        connection.close()
        return save_application(data)  # try again with new number

    except Exception as e:
        print("[DATABASE] Unexpected error in save_application:", repr(e))
        raise

    finally:
        try:
            connection.close()
        except:
            pass


#Step 4: Start the server
        
def start_server():                       #This is the main server function which listens for clients

    #Create database first
    create_database()

    #Server Configuration
    HOST = '127.0.0.1'                    #localhost as server runs on my computer
    PORT = 65432                          #Port Number (I can use any port from 49152 to 65535)

    #Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Allowing the reuse of address it is helpul during the testing
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Binding socket to address and port
    server_socket.bind((HOST, PORT))

    #Listening for connections (maximum 5 in queue)
    server_socket.listen(5)

    print("="* 60)
    print("DBS Application SERVER - RUNNING")
    print("=" * 60)
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    print("[SERVER] Waiting for student applications...")
    print("=" * 60)

    try:
        while True:              #Keep server running forever
            #Accept client connection
            client_socket, client_address = server_socket.accept()
            print(f"\n[CONNECTION] New connection from {client_address}")

            try:
                #Receive data from client (max 4096 bytes)
                data = client_socket.recv(4096).decode('utf-8')

                if data:
                    print(f"[RECEIVED] Data received from client")

                    #Convert JSON string back to dictionary
                    application_data = json.loads(data)

                    #Displaying received data
                    print("\n--- APPLICATION DETAILS ---")
                    print(f"Name:  {application_data['name']}")
                    print(f"Course: {application_data['course']}")
                    print(f"Start: {application_data['start_month']} {application_data['start_year']}")
                    print("--------------------------")

                    #Save to database and get application number
                    app_number = save_application(application_data)

                    #Send application number back to client
                    response = json.dumps({
                        'status': 'success',
                        'application_number': app_number,
                        'message': 'Application submitted successfully!'
                    })

                    client_socket.send(response.encode('utf-8'))
                    print(f"[SENT] Application number sent to client: {app_number}\n")

            except json.JSONDecodeError:
                #Handling invalid data format
                error_response = json.dumps({
                    'status': 'error',
                    'message' : 'Invalid data format'
                })
                client_socket.send(error_response.encode('utf-8'))
                print("[ERROR] Invalid data received")

            except Exception as e:
                #Handling any other errors
                error_response = json.dumps({
                    'status': 'error',
                    'message': str(e)
                })
                client_socket.send(error_response.encode('utf-8'))
                print(f"[ERROR] {e}")

            finally:
                #Closing client connection
                client_socket.close()
                print("[CONNECTION] Client disconnected")

    except KeyboardInterrupt:
        #Handle Ctrl+C to stop the server
        print("\n\n[SERVER] Shutting down...")
        server_socket.close()
        print("[SERVER] Server stopped")

#Running the server

if __name__ == "__main__":
    start_server()


            

        


