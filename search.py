import json
import sqlite3
from tabulate import tabulate

def reconstruct_json_from_sqlite(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all rows from the table
    cursor.execute("SELECT * FROM Events")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Process rows and construct JSON data
    json_data = []
    for row in rows:
        row_dict = dict(zip(column_names, row))

        # Extract and process the 'info' section
        info = {}
        if row_dict["Issuer"]:
            info["Issuer"] = row_dict["Issuer"].split(" | ")
        if row_dict["Acquirer"]:
            info["Acquirer"] = row_dict["Acquirer"].split(" | ")
        if row_dict["Tier"]:
            info["Tier"] = row_dict["Tier"].split(" | ")
        if row_dict["TierEndingValue"]:
            info["TierEndingValue"] = row_dict["TierEndingValue"].split(" | ")
        if row_dict["Rate"]:
            info["Rate"] = row_dict["Rate"].split(" | ")

        # Construct the main entry
        entry = {
            "identifier": row_dict["identifier"],
            "heading": row_dict["heading"],
            "description": row_dict["description"],
            "UniqueCode": row_dict["UniqueCode"],
            "category": row_dict["category"],
            "info": info if info else None  # Set to None if no info is available
        }

        # Append the entry to the JSON data
        json_data.append(entry)

    # Close the database connection
    conn.close()

    # Return the reconstructed JSON data
    return json_data

# function to print details of a selected identifier
def get_details(selected_data, filter_country=None):
    details = {
        "heading": selected_data.get("heading"),
        "description": selected_data.get("description"),
        "unique_code": selected_data.get("UniqueCode"),
        "category": selected_data.get("category", "None"),
        "info_table": None,
    }

    info = selected_data.get("info", {})
    if info:
        headers = list(info.keys())
        rows = list(zip(*[info[key] for key in headers]))

        # apply filter if provided
        if filter_country:
            rows = [row for row in rows if row[headers.index("Issuer")].strip().lower() == filter_country.strip().lower()]
        
        if rows:
            numbered_rows = [(i + 1, *row) for i, row in enumerate(rows)]
            headers_with_numbers = ["#", *headers]
            details["info_table"] = {
                "headers": headers_with_numbers,
                "rows": numbered_rows,
            }
    
    return details

# function to search by issuer
def search_by_issuer(filter_country, data_dict):
    results = []
    for identifier, entry in data_dict.items():
        info = entry.get("info", {})
        if info and "Issuer" in info:
            rows = list(zip(*[info[key] for key in info.keys()]))
            filtered_rows = [row for row in rows if row[list(info.keys()).index("Issuer")].strip().lower() == filter_country.strip().lower()]

            if filtered_rows:
                details = {
                    "identifier": identifier,
                    "heading": entry.get("heading"),
                    "unique_code": entry.get("UniqueCode"),
                    "info_table": {
                        "headers": ["#", *info.keys()],
                        "rows": [(i + 1, *row) for i, row in enumerate(filtered_rows)],
                    },
                }
                results.append(details)
    
    return results

# main loop for user input
def main():
    # # load data with JSON file
    # with open('PdfData.json', 'r') as f:
    #     data = json.load(f)

    # Load data with SQLite file
    db_path = "data.sqlite" 
    data = reconstruct_json_from_sqlite(db_path)

    # preprocess data into a dictionary for quick lookup
    data_dict = {item['identifier']: item for item in data}
    identifiers = list(data_dict.keys())

    while True:
        print("\n--- Main Menu ---")
        print("1. Search by Identifier")
        print("2. Search by Issuer")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            while True:
                print("\nAvailable Identifiers:")
                print(", ".join(identifiers))
                selected_option = input("Enter an Identifier (or type 'exit' to quit): ").strip()
                
                if selected_option.lower() == "exit":
                    break
                
                if selected_option in data_dict:
                    selected_data = data_dict[selected_option]
                    filter_country = input("\nEnter a country to filter by Issuer (or press Enter to skip): ").strip()
                    details = get_details(selected_data, filter_country or None)
                    
                    print("\n--- Details ---")
                    print(f"Heading: {details['heading']}")
                    print(f"Description: {details['description']}")
                    print(f"Unique Code: {details['unique_code']}")
                    if details["category"] != "None":
                        print(f"Category: {details['category']}")
                    
                    if details["info_table"]:
                        print("\n--- Info Table ---")
                        print(tabulate(details["info_table"]["rows"], headers=details["info_table"]["headers"], tablefmt="grid"))
                    else:
                        print("No additional info available for this identifier.")
                else:
                    print(f"Identifier '{selected_option}' not found. Please try again.")

        elif choice == "2":
            filter_country = input("\nEnter a country to filter by Issuer: ").strip().lower()
            if not filter_country:
                print("No country provided. Returning to main menu.")
                continue
            
            results = search_by_issuer(filter_country, data_dict)
            if results:
                for result in results:
                    print(f"\nIdentifier: {result['identifier']}")
                    print(f"Heading: {result['heading']}")
                    print(f"Unique Code: {result['unique_code']}")
                    print("\n--- Info Table ---")
                    print(tabulate(result["info_table"]["rows"], headers=result["info_table"]["headers"], tablefmt="grid"))
            else:
                print(f"No entries found where Issuer is '{filter_country}'.")

        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()