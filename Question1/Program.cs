using System;
using System.Collections.Generic;
using System.Linq;

namespace ContactBookApp
{
    // Contact class represents a single contact with encapsulation
    class Contact
    {
        // Private fields - demonstrating encapsulation
        private string firstName;
        private string lastName;
        private string company;
        private string mobileNumber;
        private string email;
        private DateTime birthdate;

        // Properties with validation - demonstrating properties and access modifiers
        public string FirstName
        {
            get { return firstName; }
            set { firstName = value; }
        }

        public string LastName
        {
            get { return lastName; }
            set { lastName = value; }
        }

        public string Company
        {
            get { return company; }
            set { company = value; }
        }

        public string MobileNumber
        {
            get { return mobileNumber; }
            set
            {
                // Validation: must be 9 digits, positive, non-zero
                if (IsValidMobileNumber(value))
                {
                    mobileNumber = value;
                }
                else
                {
                    throw new ArgumentException("Invalid mobile number. Must be 9 digits.");
                }
            }
        }

        public string Email
        {
            get { return email; }
            set { email = value; }
        }

        public DateTime Birthdate
        {
            get { return birthdate; }
            set { birthdate = value; }
        }

        // Constructor - demonstrating object creation
        public Contact(string firstName, string lastName, string company, 
                      string mobileNumber, string email, DateTime birthdate)
        {
            FirstName = firstName;
            LastName = lastName;
            Company = company;
            MobileNumber = mobileNumber; // Will validate through property
            Email = email;
            Birthdate = birthdate;
        }

        // Method to validate mobile number
        private bool IsValidMobileNumber(string number)
        {
            // Check if exactly 9 digits and all characters are digits
            if (string.IsNullOrEmpty(number) || number.Length != 9)
                return false;

            foreach (char c in number)
            {
                if (!char.IsDigit(c))
                    return false;
            }

            // Check if it's not all zeros
            if (number == "000000000")
                return false;

            return true;
        }

        // Method overloading - Display with and without index
        public void Display()
        {
            Console.WriteLine($"Name: {FirstName} {LastName}");
            Console.WriteLine($"Company: {Company}");
            Console.WriteLine($"Mobile: {MobileNumber}");
            Console.WriteLine($"Email: {Email}");
            Console.WriteLine($"Birthdate: {Birthdate.ToShortDateString()}");
            Console.WriteLine("----------------------------------------");
        }

        public void Display(int index)
        {
            Console.WriteLine($"\n[{index}] {FirstName} {LastName}");
            Console.WriteLine($"    Company: {Company}");
            Console.WriteLine($"    Mobile: {MobileNumber}");
            Console.WriteLine($"    Email: {Email}");
            Console.WriteLine($"    Birthdate: {Birthdate.ToShortDateString()}");
        }
    }

    // ContactBook class manages all contacts - demonstrating object relationships
    class ContactBook
    {
        // Using List as data structure to store contacts
        private List<Contact> contacts;

        // Constructor
        public ContactBook()
        {
            contacts = new List<Contact>();
            InitializeContacts(); // Add 20 sample contacts
        }

        // Initialize with 20 sample contacts
        private void InitializeContacts()
        {
            string[] firstNames = { "Emily", "John", "Sarah", "Michael", "Jessica",
                                   "David", "Emma", "Daniel", "Olivia", "James",
                                   "Sophia", "William", "Isabella", "Robert", "Mia",
                                   "Thomas", "Charlotte", "Christopher", "Amelia", "Matthew" };

            string[] lastNames = { "Smith", "Johnson", "Williams", "Brown", "Jones",
                                  "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                                  "Thomas", "Taylor", "Moore", "Jackson", "Martin" };

            for (int i = 0; i < 20; i++)
            {
                try
                {
                    Contact contact = new Contact(
                        firstNames[i],
                        lastNames[i],
                        "Dublin Business School",
                        $"08{7000000 + i + 1000}", // Generates valid 9-digit numbers
                        $"{firstNames[i].ToLower()}.{lastNames[i].ToLower()}@dbs.ie",
                        new DateTime(1985 + i % 10, (i % 12) + 1, (i % 28) + 1)
                    );
                    contacts.Add(contact);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error adding contact: {ex.Message}");
                }
            }
        }

        // Add new contact
        public void AddContact()
        {
            try
            {
                Console.WriteLine("\n--- Add New Contact ---");
                
                Console.Write("First Name: ");
                string firstName = Console.ReadLine();

                Console.Write("Last Name: ");
                string lastName = Console.ReadLine();

                Console.Write("Company: ");
                string company = Console.ReadLine();

                Console.Write("Mobile Number (9 digits): ");
                string mobile = Console.ReadLine();

                Console.Write("Email: ");
                string email = Console.ReadLine();

                Console.Write("Birthdate (dd/MM/yyyy): ");
                DateTime birthdate = DateTime.Parse(Console.ReadLine());

                Contact newContact = new Contact(firstName, lastName, company, 
                                                mobile, email, birthdate);
                contacts.Add(newContact);
                
                Console.WriteLine("\n✓ Contact added successfully!");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"\n✗ Error: {ex.Message}");
            }
            catch (FormatException)
            {
                Console.WriteLine("\n✗ Error: Invalid date format. Please use dd/MM/yyyy");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n✗ Unexpected error: {ex.Message}");
            }
        }

        // Show all contacts - basic list
        public void ShowAllContacts()
        {
            if (contacts.Count == 0)
            {
                Console.WriteLine("\nNo contacts found.");
                return;
            }

            Console.WriteLine($"\n--- All Contacts ({contacts.Count}) ---");
            for (int i = 0; i < contacts.Count; i++)
            {
                contacts[i].Display(i + 1);
            }
        }

        // Show detailed contact information
        public void ShowContactDetails()
        {
            if (contacts.Count == 0)
            {
                Console.WriteLine("\nNo contacts available.");
                return;
            }

            Console.Write("\nEnter contact number to view: ");
            if (int.TryParse(Console.ReadLine(), out int index))
            {
                index--; // Adjust for 0-based indexing
                
                if (index >= 0 && index < contacts.Count)
                {
                    Console.WriteLine("\n--- Contact Details ---");
                    contacts[index].Display();
                }
                else
                {
                    Console.WriteLine("\n✗ Invalid contact number.");
                }
            }
            else
            {
                Console.WriteLine("\n✗ Please enter a valid number.");
            }
        }

        // Update contact information
        public void UpdateContact()
        {
            if (contacts.Count == 0)
            {
                Console.WriteLine("\nNo contacts to update.");
                return;
            }

            ShowAllContacts();
            
            Console.Write("\nEnter contact number to update: ");
            if (int.TryParse(Console.ReadLine(), out int index))
            {
                index--;
                
                if (index >= 0 && index < contacts.Count)
                {
                    try
                    {
                        Console.WriteLine("\n--- Update Contact (press Enter to keep current value) ---");
                        
                        Console.Write($"First Name [{contacts[index].FirstName}]: ");
                        string input = Console.ReadLine();
                        if (!string.IsNullOrWhiteSpace(input))
                            contacts[index].FirstName = input;

                        Console.Write($"Last Name [{contacts[index].LastName}]: ");
                        input = Console.ReadLine();
                        if (!string.IsNullOrWhiteSpace(input))
                            contacts[index].LastName = input;

                        Console.Write($"Company [{contacts[index].Company}]: ");
                        input = Console.ReadLine();
                        if (!string.IsNullOrWhiteSpace(input))
                            contacts[index].Company = input;

                        Console.Write($"Mobile [{contacts[index].MobileNumber}]: ");
                        input = Console.ReadLine();
                        if (!string.IsNullOrWhiteSpace(input))
                            contacts[index].MobileNumber = input;

                        Console.Write($"Email [{contacts[index].Email}]: ");
                        input = Console.ReadLine();
                        if (!string.IsNullOrWhiteSpace(input))
                            contacts[index].Email = input;

                        Console.WriteLine("\n✓ Contact updated successfully!");
                    }
                    catch (ArgumentException ex)
                    {
                        Console.WriteLine($"\n✗ Update failed: {ex.Message}");
                    }
                }
                else
                {
                    Console.WriteLine("\n✗ Invalid contact number.");
                }
            }
            else
            {
                Console.WriteLine("\n✗ Please enter a valid number.");
            }
        }

        // Delete contact
        public void DeleteContact()
        {
            if (contacts.Count == 0)
            {
                Console.WriteLine("\nNo contacts to delete.");
                return;
            }

            ShowAllContacts();
            
            Console.Write("\nEnter contact number to delete: ");
            if (int.TryParse(Console.ReadLine(), out int index))
            {
                index--;
                
                if (index >= 0 && index < contacts.Count)
                {
                    string name = $"{contacts[index].FirstName} {contacts[index].LastName}";
                    contacts.RemoveAt(index);
                    Console.WriteLine($"\n✓ Contact '{name}' deleted successfully!");
                }
                else
                {
                    Console.WriteLine("\n✗ Invalid contact number.");
                }
            }
            else
            {
                Console.WriteLine("\n✗ Please enter a valid number.");
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            ContactBook contactBook = new ContactBook();
            bool running = true;

            Console.WriteLine("╔════════════════════════════════════════╗");
            Console.WriteLine("║    CONTACT BOOK MANAGEMENT SYSTEM      ║");
            Console.WriteLine("╚════════════════════════════════════════╝");

            while (running)
            {
                Console.WriteLine("\n- - - - - - - - - - - - - - - - - - - -");
                Console.WriteLine("Main Menu");
                Console.WriteLine("1: Add Contact");
                Console.WriteLine("2: Show All Contacts");
                Console.WriteLine("3: Show Contact Details");
                Console.WriteLine("4: Update Contact");
                Console.WriteLine("5: Delete Contact");
                Console.WriteLine("0: Exit");
                Console.WriteLine("- - - - - - - - - - - - - - - - - - - -");
                Console.Write("Enter your choice: ");

                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        contactBook.AddContact();
                        break;
                    case "2":
                        contactBook.ShowAllContacts();
                        break;
                    case "3":
                        contactBook.ShowContactDetails();
                        break;
                    case "4":
                        contactBook.UpdateContact();
                        break;
                    case "5":
                        contactBook.DeleteContact();
                        break;
                    case "0":
                        Console.WriteLine("\nThank you for using Contact Book!");
                        running = false;
                        break;
                    default:
                        Console.WriteLine("\n✗ Invalid choice. Please try again.");
                        break;
                }
            }
        }
    }
}