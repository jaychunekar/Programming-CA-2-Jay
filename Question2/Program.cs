using System;
using System.Collections.Generic;

namespace FileExtensionInfo
{
    // FileExtension class to store information about each file type
    class FileExtension
    {
        // Private fields - encapsulation
        private string extension;
        private string description;
        private string category;
        private string commonUse;

        // Properties with access modifiers
        public string Extension
        {
            get { return extension; }
            set { extension = value; }
        }

        public string Description
        {
            get { return description; }
            set { description = value; }
        }

        public string Category
        {
            get { return category; }
            set { category = value; }
        }

        public string CommonUse
        {
            get { return commonUse; }
            set { commonUse = value; }
        }

        // Constructor
        public FileExtension(string ext, string desc, string cat, string use)
        {
            Extension = ext;
            Description = desc;
            Category = cat;
            CommonUse = use;
        }

        // Method overloading - Display with different formats
        public void Display()
        {
            Console.WriteLine($"\n╔════════════════════════════════════════════════════╗");
            Console.WriteLine($"  Extension: {Extension}");
            Console.WriteLine($"  Description: {Description}");
            Console.WriteLine($"  Category: {Category}");
            Console.WriteLine($"  Common Use: {CommonUse}");
            Console.WriteLine($"╚════════════════════════════════════════════════════╝");
        }

        public void Display(bool brief)
        {
            if (brief)
            {
                Console.WriteLine($"{Extension} - {Description}");
            }
            else
            {
                Display();
            }
        }
    }

    // FileExtensionSystem class manages all file extensions
    class FileExtensionSystem
    {
        // Dictionary data structure for fast lookup by extension name
        private Dictionary<string, FileExtension> extensions;

        // Constructor - initializes with 20+ file extensions
        public FileExtensionSystem()
        {
            extensions = new Dictionary<string, FileExtension>();
            InitializeExtensions();
        }

        // Initialize the system with 20+ file extensions
        private void InitializeExtensions()
        {
            // Video formats
            AddExtension("mp4", "MPEG-4 Video", "Video", 
                "Widely used for video streaming and storage");
            AddExtension("mov", "QuickTime Movie", "Video", 
                "Apple's video format, high quality");
            AddExtension("avi", "Audio Video Interleave", "Video", 
                "Microsoft video format, good compatibility");
            AddExtension("mkv", "Matroska Video", "Video", 
                "Open-source format, supports multiple audio/subtitle tracks");
            AddExtension("webm", "WebM Video", "Video", 
                "Web-optimized video format");

            // Image formats
            AddExtension("jpg", "Joint Photographic Experts Group", "Image", 
                "Compressed image format, widely used for photos");
            AddExtension("png", "Portable Network Graphics", "Image", 
                "Lossless compression, supports transparency");
            AddExtension("gif", "Graphics Interchange Format", "Image", 
                "Supports animation, limited colors");
            AddExtension("svg", "Scalable Vector Graphics", "Image", 
                "Vector image format, scales without quality loss");
            AddExtension("bmp", "Bitmap Image", "Image", 
                "Uncompressed image format");

            // Audio formats
            AddExtension("mp3", "MPEG Audio Layer 3", "Audio", 
                "Compressed audio, most popular music format");
            AddExtension("wav", "Waveform Audio", "Audio", 
                "Uncompressed audio, high quality");
            AddExtension("flac", "Free Lossless Audio Codec", "Audio", 
                "Lossless compression, audiophile choice");
            AddExtension("aac", "Advanced Audio Coding", "Audio", 
                "Modern compressed audio format");

            // Document formats
            AddExtension("pdf", "Portable Document Format", "Document", 
                "Universal document format, preserves formatting");
            AddExtension("docx", "Microsoft Word Document", "Document", 
                "Word processing document");
            AddExtension("xlsx", "Microsoft Excel Spreadsheet", "Document", 
                "Spreadsheet for data and calculations");
            AddExtension("pptx", "Microsoft PowerPoint Presentation", "Document", 
                "Presentation slides");
            AddExtension("txt", "Plain Text", "Document", 
                "Simple unformatted text");

            // Programming/Web formats
            AddExtension("html", "HyperText Markup Language", "Web", 
                "Web page structure and content");
            AddExtension("css", "Cascading Style Sheets", "Web", 
                "Styling for web pages");
            AddExtension("js", "JavaScript", "Programming", 
                "Web programming and interactivity");
            AddExtension("py", "Python Script", "Programming", 
                "Python programming language");
            AddExtension("cs", "C# Source Code", "Programming", 
                "C# programming language");
            AddExtension("json", "JavaScript Object Notation", "Data", 
                "Data interchange format");
        }

        // Helper method to add extension to dictionary
        private void AddExtension(string ext, string desc, string cat, string use)
        {
            extensions[ext.ToLower()] = new FileExtension(
                "." + ext, desc, cat, use);
        }

        // Search for extension information
        public void SearchExtension(string query)
        {
            // Remove dot if user includes it
            query = query.TrimStart('.').ToLower();

            if (extensions.ContainsKey(query))
            {
                Console.WriteLine("\n✓ Extension found!");
                extensions[query].Display();
            }
            else
            {
                HandleUnknownExtension(query);
            }
        }

        // Handle unknown extensions gracefully
        private void HandleUnknownExtension(string ext)
        {
            Console.WriteLine($"\n╔════════════════════════════════════════════════════╗");
            Console.WriteLine($"  ✗ Extension '.{ext}' not found in database.");
            Console.WriteLine($"  ");
            Console.WriteLine($"  This could be:");
            Console.WriteLine($"  • A less common file format");
            Console.WriteLine($"  • A typo in the extension name");
            Console.WriteLine($"  • A custom or proprietary format");
            Console.WriteLine($"  ");
            Console.WriteLine($"  Suggestion: Try browsing all extensions (Option 2)");
            Console.WriteLine($"╚════════════════════════════════════════════════════╝");
        }

        // Show all available extensions
        public void ShowAllExtensions()
        {
            Console.WriteLine($"\n╔════════════════════════════════════════════════════╗");
            Console.WriteLine($"  Available File Extensions ({extensions.Count} total)");
            Console.WriteLine($"╚════════════════════════════════════════════════════╝");

            // Group by category
            var categories = new Dictionary<string, List<FileExtension>>();
            
            foreach (var ext in extensions.Values)
            {
                if (!categories.ContainsKey(ext.Category))
                {
                    categories[ext.Category] = new List<FileExtension>();
                }
                categories[ext.Category].Add(ext);
            }

            // Display grouped by category
            foreach (var category in categories)
            {
                Console.WriteLine($"\n{category.Key}:");
                Console.WriteLine(new string('-', 50));
                foreach (var ext in category.Value)
                {
                    Console.WriteLine($"  {ext.Extension,-8} - {ext.Description}");
                }
            }
        }

        // Show extensions by category
        public void ShowByCategory()
        {
            Console.WriteLine("\nAvailable Categories:");
            Console.WriteLine("1. Video");
            Console.WriteLine("2. Image");
            Console.WriteLine("3. Audio");
            Console.WriteLine("4. Document");
            Console.WriteLine("5. Web");
            Console.WriteLine("6. Programming");
            Console.WriteLine("7. Data");
            
            Console.Write("\nEnter category number: ");
            string choice = Console.ReadLine();

            string categoryName = choice switch
            {
                "1" => "Video",
                "2" => "Image",
                "3" => "Audio",
                "4" => "Document",
                "5" => "Web",
                "6" => "Programming",
                "7" => "Data",
                _ => null
            };

            if (categoryName != null)
            {
                Console.WriteLine($"\n{categoryName} File Extensions:");
                Console.WriteLine(new string('-', 50));
                
                bool found = false;
                foreach (var ext in extensions.Values)
                {
                    if (ext.Category == categoryName)
                    {
                        ext.Display(true); // Brief display
                        found = true;
                    }
                }

                if (!found)
                {
                    Console.WriteLine("No extensions found in this category.");
                }
            }
            else
            {
                Console.WriteLine("\n✗ Invalid category choice.");
            }
        }

        // Get count of extensions
        public int GetExtensionCount()
        {
            return extensions.Count;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            FileExtensionSystem system = new FileExtensionSystem();

            Console.WriteLine("╔════════════════════════════════════════════════════╗");
            Console.WriteLine("║     FILE EXTENSION INFORMATION SYSTEM              ║");
            Console.WriteLine("╚════════════════════════════════════════════════════╝");
            Console.WriteLine($"\nDatabase contains {system.GetExtensionCount()} file extensions");

            bool running = true;

            while (running)
            {
                Console.WriteLine("\n════════════════════════════════════════════════════");
                Console.WriteLine("Main Menu:");
                Console.WriteLine("1. Search for file extension");
                Console.WriteLine("2. Show all extensions");
                Console.WriteLine("3. Browse by category");
                Console.WriteLine("0. Exit");
                Console.WriteLine("════════════════════════════════════════════════════");
                Console.Write("Enter your choice: ");

                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        Console.Write("\nEnter file extension (e.g., mp4 or .mp4): ");
                        string query = Console.ReadLine();
                        
                        if (!string.IsNullOrWhiteSpace(query))
                        {
                            system.SearchExtension(query);
                        }
                        else
                        {
                            Console.WriteLine("\n✗ Please enter a valid extension.");
                        }
                        break;

                    case "2":
                        system.ShowAllExtensions();
                        break;

                    case "3":
                        system.ShowByCategory();
                        break;

                    case "0":
                        Console.WriteLine("\n✓ Thank you for using File Extension System!");
                        running = false;
                        break;

                    default:
                        Console.WriteLine("\n✗ Invalid choice. Please select 0-3.");
                        break;
                }

                if (running)
                {
                    Console.WriteLine("\nPress any key to continue...");
                    Console.ReadKey();
                    Console.Clear();
                    Console.WriteLine("╔════════════════════════════════════════════════════╗");
                    Console.WriteLine("║     FILE EXTENSION INFORMATION SYSTEM              ║");
                    Console.WriteLine("╚════════════════════════════════════════════════════╝");
                }
            }
        }
    }
}