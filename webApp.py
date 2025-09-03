#
# To run this app, run `pip install - requirements.txt`
# Then, `python -m streamlit run webApp.py`
# The web app should open in http://localhost:8501
#

import streamlit as st
import json
import pandas as pd

st.title("Database Searching App")
st.markdown("""
This tool is used to search the data contents from the PDF file.
""")

# Load JSON data
with open('pdfData.json', 'r') as f:
    data = json.load(f)

# Preprocess data into a dictionary for quick lookup
data_dict = {item['identifier']: item for item in data}

# Extract all identifiers for the dropdown
options = list(data_dict.keys())

# Dropdown for selecting an identifier
selected_option = st.selectbox(
    "Select an Identifier:",
    options,
    index=None,
    placeholder="Choose an identifier"
)

# Display details if an identifier is selected
if selected_option:
    selected_data = data_dict.get(selected_option)
    if selected_data:
        # Display Heading, Description, UniqueCode, and Category (if not "None")
        st.markdown(f"### {selected_data['heading']} `{selected_data['UniqueCode']}`")
        st.markdown(f"{selected_data['description']}")
        if selected_data['category'] != "None":
            st.markdown(f"**Category:** `{selected_data['category']}`")

        # Prepare the info section for the table
        info = selected_data.get("info", {})
        if info:
            # Convert info into a DataFrame for table display
            table_data = {}
            for key, values in info.items():
                table_data[key] = values

            # Ensure all lists are of the same length by padding with empty strings
            max_length = max(len(values) for values in table_data.values())
            for key in table_data:
                table_data[key] += [""] * (max_length - len(table_data[key]))

            # Create a DataFrame
            df = pd.DataFrame(table_data)

            # Reset index to start from 1 instead of 0
            df.index = df.index + 1

            # Rename the index column to "#" for brevity
            df.index.name = "#"

            # Display the table
            st.markdown("***")
            st.markdown("### **Info Table:**")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No additional info available for this identifier.")
    else:
        st.error("No data found for the selected identifier.")



