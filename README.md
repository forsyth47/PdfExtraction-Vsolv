# PDF Extraction and Search System

A comprehensive Python-based system for extracting, processing, and searching structured data from PDF documents. This project provides both console and web-based interfaces for interacting with extracted PDF data.

## 🚀 Project Overview

This system extracts structured text data from PDF documents, processes it into a searchable format, and provides multiple interfaces for data retrieval. It's particularly useful for processing financial documents, reports, or any PDF containing structured information with identifiers, rates, and categorized data.

### Key Features

- **Advanced PDF Text Extraction**: Uses PyMuPDF for comprehensive text extraction with metadata preservation
- **Intelligent Data Parsing**: Regex-based pattern recognition to identify and structure data
- **Dual Storage System**: Saves data in both JSON and SQLite formats
- **Multiple Search Interfaces**: Console-based CLI and modern web interface
- **Flexible Search Options**: Search by identifier or issuer with filtering capabilities
- **Rich Data Display**: Formatted tables with detailed information presentation

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Detailed Usage](#detailed-usage)
- [Data Flow](#data-flow)
- [Code Documentation](#code-documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/forsyth47/PdfExtraction-Vsolv.git
cd PdfExtraction-Vsolv
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `pymupdf` - Advanced PDF processing and text extraction
- `tabulate` - Console table formatting for readable output
- `streamlit` - Modern web application framework

### Step 3: Verify Installation

```bash
python -c "import pymupdf, tabulate, streamlit; print('All dependencies installed successfully!')"
```

## 🚦 Quick Start

### 1. Verify Installation

Run the comprehensive test suite to ensure everything is set up correctly:

```bash
python test_system.py
```

This will check:
- ✅ All dependencies are installed
- ✅ PDF file is present
- ✅ Data generation works correctly
- ✅ JSON and database files are created properly
- ✅ Search and web app scripts are functional

### 2. Generate Data from PDF

Extract and process data from the included PDF:

```bash
python generateData.py
```

This creates:
- `pdfData.json` - Structured JSON data
- `data.sqlite` - SQLite database for efficient querying

### 3. Search Using Console Interface

```bash
python search.py
```

### 4. Launch Web Application

```bash
streamlit run webApp.py
```

Access the web interface at `http://localhost:8501`

### 5. Quick Development Server

Use the provided development server script:

```bash
./devserver.sh
```

This script will:
- Activate virtual environment (if present)
- Install dependencies
- Generate data (if not already present)
- Start the Streamlit web application

## 📁 Project Structure

```
PdfExtraction-Vsolv/
├── generateData.py      # Core PDF extraction and processing
├── search.py           # Console-based search interface
├── webApp.py          # Streamlit web application
├── test_system.py     # Comprehensive test suite
├── requirements.txt    # Python dependencies
├── data.pdf           # Sample PDF document
├── devserver.sh       # Development server script
├── .gitignore         # Git ignore patterns
├── .idx/              # Index directory
└── README.md          # This documentation
```

### Generated Files (after running generateData.py)

```
├── pdfData.json       # Extracted data in JSON format
└── data.sqlite        # SQLite database for search operations
```

## 📖 Detailed Usage

### Data Generation (`generateData.py`)

This is the core component that processes PDF documents and extracts structured data.

#### How it works:

1. **PDF Reading**: Uses PyMuPDF to read the PDF and extract text with detailed metadata
2. **Text Processing**: Applies intelligent parsing to identify:
   - Identification codes (alphanumeric patterns)
   - Headings and descriptions
   - Unique codes and categories
   - Rate information (Issuer, Acquirer, Tier data)
3. **Data Structuring**: Organizes extracted information into consistent JSON objects
4. **Database Storage**: Saves processed data to SQLite database for efficient querying

#### Usage:

```bash
python generateData.py
```

#### Key Functions:

- `rawDataExtractionWithMetadata(pdf_path)` - Extracts raw text with formatting metadata
- `parseRawDataWithMetadata(raw_data)` - Processes and structures the raw data
- `json_to_sqlite(json_file, db_file)` - Converts JSON data to SQLite database

### Console Search Interface (`search.py`)

Interactive command-line tool for searching and displaying extracted data.

#### Features:

- **Search by Identifier**: Find specific entries using their unique identifiers
- **Search by Issuer**: Filter entries by issuer country/region
- **Detailed Display**: Shows complete information including rates, tiers, and categories
- **Interactive Menu**: User-friendly navigation system

#### Usage:

```bash
python search.py
```

#### Menu Options:

1. **Search by Identifier**
   - Lists all available identifiers
   - Allows selection and detailed viewing
   - Optional filtering by issuer country

2. **Search by Issuer**
   - Filter all entries by issuer name
   - Shows matching entries with rate information
   - Displays formatted tables

3. **Exit**
   - Safely closes the application

#### Example Session:

```
--- Main Menu ---
1. Search by Identifier
2. Search by Issuer  
3. Exit
Enter your choice (1/2/3): 1

Available Identifiers:
21M3XYZ, 28L9SOP, 23K4SOI5T, 26H5SOK8T, ...

Enter an Identifier (or type 'exit' to quit): 21M3XYZ
Enter a country to filter by Issuer (or press Enter to skip): India

--- Details ---
Heading: Adherence to commonly accepted moral
Description: This ethical standards and actions that promote honesty and decency.
Unique Code: 1L

--- Info Table ---
+---+--------+----------+
| # | Issuer | Rate     |
+===+========+==========+
| 1 | India  | USD 250.00 |
+---+--------+----------+
```

### Web Application (`webApp.py`)

Modern Streamlit-based web interface providing an intuitive way to browse and search data.

#### Features:

- **Interactive Dropdown**: Select identifiers from a searchable dropdown menu
- **Rich Display**: Formatted presentation of all data fields
- **Responsive Tables**: Interactive data tables with pandas integration
- **Real-time Search**: Instant results as you select different identifiers

#### Usage:

```bash
streamlit run webApp.py
```

#### Interface Components:

1. **Title and Description**: Clear explanation of the tool's purpose
2. **Identifier Selector**: Dropdown menu with all available identifiers
3. **Detail Display**: 
   - Heading with unique code
   - Full description
   - Category information (when applicable)
   - Info table with rates, issuers, and other details

#### Web Interface Features:

- Clean, professional design
- Mobile-responsive layout
- Fast search and filtering
- Exportable data tables
- Bookmark-able URLs for specific entries

## 🔄 Data Flow

```
PDF Document (data.pdf)
        ↓
    generateData.py
        ↓
   [Text Extraction]
   [Metadata Processing]
   [Pattern Recognition]
   [Data Structuring]
        ↓
    ┌─────────────┐    ┌──────────────┐
    │ pdfData.json │    │ data.sqlite  │
    └─────────────┘    └──────────────┘
           ↓                    ↓
      webApp.py            search.py
    (Streamlit Web)    (Console Interface)
           ↓                    ↓
     Web Browser          Command Line
```

## 🔧 Code Documentation

### Data Structure

Each extracted entry follows this structure:

```json
{
    "identifier": "21M3XYZ",           // Unique alphanumeric identifier
    "heading": "Document heading",      // Main title/heading
    "description": "Detailed text",    // Full description
    "UniqueCode": "1L",                // Short unique code
    "category": "Category Name",        // Classification (or "None")
    "info": {                          // Additional structured data
        "Issuer": ["Country/Region"],   // Issuing entity
        "Rate": ["USD 250.00"],        // Associated rates
        "Acquirer": ["Entity Name"],    // Acquiring entity (optional)
        "Tier": ["Tier Level"],        // Tier information (optional)
        "TierEndingValue": ["Value"]    // Tier ending values (optional)
    }
}
```

### Key Processing Logic

#### Identifier Recognition
- Uses regex pattern `^[A-Z0-9]{7,}$` to identify entry codes
- Requires text formatting flags ≥ 16 (typically bold text)

#### Text Grouping
- Groups consecutive text until next identifier is found
- Separates description from rate information using keyword detection

#### Rate Processing
- Handles multiple rate structures:
  - Simple Issuer/Rate pairs
  - Complex Acquirer/Issuer/Rate combinations
  - Tiered rate structures with ending values

### Database Schema

SQLite table structure:

```sql
CREATE TABLE Events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier TEXT NOT NULL,
    heading TEXT,
    description TEXT,
    UniqueCode TEXT,
    category TEXT,
    Issuer TEXT,        -- Pipe-separated values
    Acquirer TEXT,      -- Pipe-separated values  
    Tier TEXT,          -- Pipe-separated values
    TierEndingValue TEXT, -- Pipe-separated values
    Rate TEXT           -- Pipe-separated values
);
```

## 📝 Examples

### Example 1: Processing a New PDF

```bash
# Place your PDF file in the project directory
cp /path/to/your/document.pdf data.pdf

# Generate data
python generateData.py

# Verify output
ls -la pdfData.json data.sqlite
```

### Example 2: Batch Processing

```python
# Custom processing script
import generateData as gd

pdf_files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

for pdf_file in pdf_files:
    print(f"Processing {pdf_file}...")
    raw_data = gd.rawDataExtractionWithMetadata(pdf_file)
    parsed_data = gd.parseRawDataWithMetadata(raw_data)
    
    # Save with custom names
    gd.json_to_sqlite(f"{pdf_file}.json", f"{pdf_file}.sqlite")
```

### Example 3: Custom Search Queries

```python
import sqlite3
import json

# Connect to database
conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

# Custom query example
cursor.execute("""
    SELECT identifier, heading, Rate 
    FROM Events 
    WHERE Issuer LIKE '%India%' 
    AND Rate LIKE '%USD%'
""")

results = cursor.fetchall()
for row in results:
    print(f"ID: {row[0]}, Heading: {row[1]}, Rate: {row[2]}")
```

## 🔍 Advanced Usage

### Custom PDF Processing

You can modify `generateData.py` to handle different PDF formats:

```python
# Modify the regex patterns for different identifier formats
identifier_pattern = r'^[A-Z0-9]{7,}$'  # Current pattern
# Change to: r'^[A-Z]{2}\d{5}$' for format like AB12345

# Adjust text processing flags
if current_flags >= 16:  # Current threshold
# Change to different values based on your PDF formatting
```

### Web App Customization

Modify `webApp.py` to add new features:

```python
# Add filtering options
filter_option = st.selectbox("Filter by Category", 
                           options=["All", "Incremental Memberships", "None"])

# Add export functionality
if st.button("Export to CSV"):
    df.to_csv("exported_data.csv", index=False)
    st.success("Data exported successfully!")
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Import Error: No module named 'pymupdf'

**Solution:**
```bash
pip install --upgrade pymupdf
# or
pip install -r requirements.txt
```

#### 2. Streamlit not starting

**Solution:**
```bash
# Check if streamlit is installed
python -c "import streamlit; print('OK')"

# If not installed
pip install streamlit

# Try alternative startup
python -m streamlit run webApp.py
```

#### 3. Empty or incorrect data extraction

**Possible causes:**
- PDF format not supported
- Text is embedded as images (OCR needed)
- Different formatting patterns

**Solutions:**
- Verify PDF contains selectable text
- Adjust regex patterns in `generateData.py`
- Check the `pageToSkip` variable for correct page handling

#### 4. Database file not found

**Solution:**
```bash
# Ensure you've run the data generation first
python generateData.py

# Check if files were created
ls -la *.json *.sqlite
```

#### 5. Web app shows "File not found" error

**Issue:** `webApp.py` looks for `PdfData.json` but the script creates `pdfData.json`

**Solution:**
Update line 18 in `webApp.py`:
```python
# Change from:
with open('PdfData.json', 'r') as f:
# To:
with open('pdfData.json', 'r') as f:
```

### Performance Optimization

#### For Large PDFs:
- Increase system memory allocation
- Process pages in batches
- Use database streaming for large datasets

#### For Multiple Files:
- Implement parallel processing
- Use database connection pooling
- Add progress bars for user feedback

### Debugging Tips

#### Enable verbose output:
```python
# Add debug prints in generateData.py
print(f"Processing page {page_num}: {len(blocks)} blocks found")
print(f"Extracted identifier: {identifier}")
```

#### Check intermediate files:
```bash
# Examine the JSON output
cat pdfData.json | python -m json.tool | head -50

# Check database contents
sqlite3 data.sqlite "SELECT * FROM Events LIMIT 5;"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly
5. Commit changes (`git commit -m 'Add new feature'`)
6. Push to branch (`git push origin feature/new-feature`)
7. Create a Pull Request

### Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt

# Run tests (if available)
python -m pytest tests/
```

## 📄 License

This project is open source. Please refer to the repository license file for full details.

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the code documentation for implementation details

---

**Built with ❤️ using Python, PyMuPDF, and Streamlit**