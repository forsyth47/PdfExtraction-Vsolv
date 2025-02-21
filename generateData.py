import pymupdf, re, json, sqlite3


def rawDataExtractionWithMetadata(pdf_path):
    print("[+] Reading Raw Data with Metadata from the PDF...")
    doc = pymupdf.open(pdf_path)
    result = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_dict = page.get_text("dict")  # Get detailed text information as a dictionary
        blocks = text_dict.get("blocks", [])  # Extract text blocks

        page_data = {
            "page_number": page_num + 1,
            "blocks": []
        }

        for block in blocks:
            if block["type"] == 0:  # Text block
                block_data = {
                    "bbox": block["bbox"],  # Bounding box of the block
                    "lines": []
                }

                for line in block.get("lines", []):
                    line_data = {
                        "spans": []
                    }

                    for span in line.get("spans", []):
                        span_data = {
                            "text": span.get("text", ""),  # The actual text
                            "font": span.get("font", ""),  # Font name
                            "size": span.get("size", 0),  # Font size
                            "color": span.get("color", 0),  # Text color (in RGB format)
                            "flags": span.get("flags", 0)  # Style flags (bold, italic, etc.)
                        }
                        line_data["spans"].append(span_data)

                    block_data["lines"].append(line_data)

                page_data["blocks"].append(block_data)

        result.append(page_data)

    # with open('raw_data.json', 'w') as file:
    #     file.write(json.dumps(raw_data, indent=4))
    print("[+] Reading Complete.")
    return result

def parseRawDataWithMetadata(raw_data):
    print("[+] Cleaning Raw Data from the PDF...")
    parsed_data = []
    final_text = []

    # Step 1: extrct txt
    pageToSkip = 1
    for page in raw_data:
        if page["page_number"] == pageToSkip:
            print(f"{'-'*8}\nSkipping page {pageToSkip}\n{'-'*8}")
            continue
        for block in page["blocks"]:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = " ".join(span["text"].strip().split())
                    if not text:
                        continue
                    if int(span['size']) == 20:
                        continue
                    # Store text and flags for later
                    final_text.append({"text": text, "flags": span.get("flags", 0)})

    #print(f"Final Text: {[item['text'] for item in final_text]}")

    # Step 2: Process `final_text` to group data by Identification Codes
    i = 0
    while i < len(final_text):
        current_item = final_text[i]
        current_line = current_item["text"]
        current_flags = current_item["flags"]

        # Check if the current line matches the Identification Code criteria
        if (
            re.match(r'^[A-Z0-9]{7,}$', current_line)  # regex uppercase alphanumeric codes
            and current_flags >= 16  # flag >= 16
        ):
            #new group
            group = [current_line]
            i += 1

            # collect all subsequent lines until next indenfi code Hufff :( // this is takin took much time :(
            while i < len(final_text):
                next_item = final_text[i]
                next_line = next_item["text"]
                next_flags = next_item["flags"]

                # stwap if next line = indeifi code
                if (
                    re.match(r'^[A-Z0-9]{7,}$', next_line)
                    and next_flags >= 16
                ):
                    break

                # UniqueID extraction
                parts = next_line.split()
                if len(parts) > 1 and len(parts[-1]) == 2 and parts[-1].isupper():
                    # cas 1: uid is part of the last word in the line
                    unique_id = parts.pop() #rm uid
                    modified_line = " ".join(parts)  #no uid line
                    group.append(modified_line)
                    group.append(unique_id) 
                else:
                    # ase 2: uid is separate element or not prst
                    group.append(next_line)

                i += 1

            # split grp in 2 subgroups: [description_part, rates_part]
            split_index = None
            for idx, line in enumerate(group):
                if "following rates apply" in line or "Tier Event ID" in line:
                    split_index = idx
                    break

            if split_index is not None:
                subgroup_1 = group[:split_index]
                subgroup_2 = group[split_index:]
                parsed_data.append([subgroup_1, subgroup_2])
            else:
                # If no split point found, append entire group as one subgroup
                parsed_data.append([group])

        else:
            # If currnt line != indenfiCode, skip it
            i += 1

    #print(f"Parsed Data: {parsed_data}")

    # stp3: process `parsed_data` to create structured entries, i.e., waste more time to make it look neat :(
    neatOutputData = []

    for group in parsed_data:
        # group = 2 subgroups: [description_part, rates_part]
        description_part = group[0]  # First subgroup
        rates_part = group[1] if len(group) > 1 else []  # 2nd index (if exists)

        identifier = description_part[0]  #1st index is always the identifier
        heading = None
        unique_code = None
        category = None
        description = []
        #reset issuer, rate, acq, tier, t_e_v for each loop
        issuer = []  
        rate = []    
        acquirer = []  
        tier = []   
        tier_ending_value = [] 
        info = {}

        # process desc
        i = 1  # Start frm 2nd index
        while i < len(description_part):
            line = description_part[i]

            # extract heading nd uniqueCode
            if heading is None:
                heading = line
                i += 1
                continue

            # extract uniqueCode
            if unique_code is None:
                if len(line) == 2 and line.isupper():
                    unique_code = line
                    i += 1
                    continue

            # extract category
            if category is None:
                if line.strip() == "Incremental":
                    category = " ".join([line, description_part[i + 1]])
                    i += 2  # skip the next as...
                    continue
                else:
                    category = "None"

            # extract description
            start_index = None
            if category.startswith("Incremental"):
                # find index with membership in it
                for idx, desc_line in enumerate(description_part):
                    if "Membership" in desc_line:
                        start_index = idx + 1
                        break
            elif unique_code is not None:
                # find index with ucode
                for idx, desc_line in enumerate(description_part):
                    if unique_code == desc_line:
                        start_index = idx + 1
                        break
            else:
                # If no ucode or latter, start frm 2nd idex
                start_index = 1

            if start_index is not None:
                # Join all elements
                description = " ".join(description_part[start_index:])
                break

            i += 1

        # process 2. rates part
        if rates_part:
            for i, line in enumerate(rates_part):
                if "Issuer" in line:
                    issuer.append(rates_part[i + 2])
                    rate.append(rates_part[i + 3])
                    break
                elif "Acquirer" in line:
                    pairs = []  
                    discarded_elements = []  
                    start_index = i + 3 
                    end_index = None

                    # Loop thru remaining lines to find grps ending with usd
                    while start_index < len(rates_part):
                        # Find nxt line containing usd
                        for j in range(start_index, len(rates_part)):
                            #print(f"Checking line: {rates_part[j]}")
                            if "USD" in rates_part[j]:
                                end_index = j
                                break

                        # disacrd if no usd in grp
                        if end_index is None:
                            discarded_elements.extend(rates_part[start_index:])
                            break

                        # grp elements
                        group = rates_part[start_index:end_index + 1]
                        pairs.append(group)

                        # update start_index for nxt grp
                        start_index = end_index + 1
                        end_index = None  # reset end_index for next loop

                    if discarded_elements:
                        print(f"Discarded these elements because no pair was found: {discarded_elements}\n")

                    # process pairs
                    for pair in pairs:
                        #print(f"Pair: {pair}")
                        rate.append(pair[-1])  
                        issuer.append(pair[-2])

                        #rest elements as the acquiererererer.
                        acquirer_parts = pair[:-2] 
                        acquirer_name = " ".join(acquirer_parts) 
                        acquirer.append(acquirer_name) 
                        #print(f"[+]Current RateList: {rate} | Current IssuerList: {issuer} | Current AcquirerList: {acquirer}")
                    break
                elif "Customer" in line:
                    acquirer.append(rates_part[i + 1])
                    rate.append(rates_part[i + 2])
                    break
                elif "Tier Event ID" in line:
                    tier_pairs = []  #grouped pairs
                    discarded_elements = [] 
                    start_index = i + 2  # srt grpin from tiereventid+2
                    end_index = None

                    # Loop thru remaining lines to find groups endin with usd
                    while start_index < len(rates_part):
                        # find nxt line w/ usd
                        for j in range(start_index, len(rates_part)):
                            if "USD" in rates_part[j]:
                                end_index = j
                                break

                        # If no usd, discard
                        if end_index is None:
                            discarded_elements.extend(rates_part[start_index:])
                            break

                        # inclusive grp elements from start_index to end_index
                        group = rates_part[start_index:end_index + 1]
                        tier_pairs.append(group)

                        # update the start_index for the nxt grp
                        start_index = end_index + 1
                        end_index = None  # reset end_index for nxt loop

                    if discarded_elements:
                        print(f"Discarded these elements because no pair was found: {discarded_elements}\n")
                    #print(f"Tier Pairs: {tier_pairs}")

                    tier = []  
                    tier_ending_value = [] 
                    rate = [] 

                    for pair in tier_pairs:
                        #print(f"Each Tier Pair: {pair}")
                        # Extract Rate (-1 element), TierEndingValue (-2 element), and Tier (-3 element)
                        rate.append(pair[-1])  
                        tier_ending_value.append(pair[-2])  
                        tier.append(pair[-3])  

                        #print(f"Current RateList: {rate} | Current TierEndingValueList: {tier_ending_value} | Current TierList: {tier}")

                    if tier or tier_ending_value or rate:
                        info["Tier"] = tier
                        info["TierEndingValue"] = tier_ending_value
                    break

        info = {}

        if len(issuer) > 0:
            info["Issuer"] = issuer
        if len(acquirer) > 0:
            info["Acquirer"] = acquirer
        if len(tier) > 0:
            info["Tier"] = tier
        if len(tier_ending_value) > 0:
            info["TierEndingValue"] = tier_ending_value
        if len(rate) > 0:
            info["Rate"] = rate

        if not bool(info)==True:
            info = None

        entry = {
            "identifier": identifier,
            "heading": heading,
            "description": description,
            "UniqueCode": unique_code,
            "category": category,
            "info": info  
        }

        #print(f"Entry: {entry}")
        neatOutputData.append(entry)

    #print(f"Neat Output Data: {neatOutputData}")
    with open('pdfData.json', 'w') as file:
        file.write(json.dumps(neatOutputData, indent=4))
    print(f"[+] Cleaning Raw Data Complete.")
    return neatOutputData

def json_to_sqlite(json_file, db_file):
    print(f"[+] Writing JSON Data to a SQLite Database...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Error reading JSON file: {e}")
        return

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT NOT NULL,
                heading TEXT,
                description TEXT,
                UniqueCode TEXT,
                category TEXT,
                Issuer TEXT,
                Acquirer TEXT,
                Tier TEXT,
                TierEndingValue TEXT,
                Rate TEXT
            )
        ''')

        for entry in data:
            identifier = entry.get("identifier", "")
            heading = entry.get("heading", "")
            description = entry.get("description", "")
            unique_code = entry.get("UniqueCode", "")
            category = entry.get("category", "")

            info = entry.get("info")
            if info is not None:
                issuer = " | ".join(info.get("Issuer", [])) if "Issuer" in info else None
                acquirer = " | ".join(info.get("Acquirer", [])) if "Acquirer" in info else None
                tier = " | ".join(info.get("Tier", [])) if "Tier" in info else None
                tier_ending_value = " | ".join(info.get("TierEndingValue", [])) if "TierEndingValue" in info else None
                rate = " | ".join(info.get("Rate", [])) if "Rate" in info else None
            else:
                issuer = None
                acquirer = None
                tier = None
                tier_ending_value = None
                rate = None

            # Insert the record into the Events table
            cursor.execute('''
                INSERT INTO Events (
                    identifier, heading, description, UniqueCode, category,
                    Issuer, Acquirer, Tier, TierEndingValue, Rate
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                identifier, heading, description, unique_code, category,
                issuer, acquirer, tier, tier_ending_value, rate
            ))

        # Step 5: Commit changes and close the connection
        conn.commit()
        conn.close()
        print("[+] Writing SQLite Database Complete.")
        print(f"[+] Data has been successfully written to {db_file}")

    except Exception as e:
        print(f"[-] Error writing to SQLite database: {e}")



inputFileName = "data.pdf"
raw_data = rawDataExtractionWithMetadata(inputFileName)
parseRawDataWithMetadata(raw_data)
json_to_sqlite("pdfData.json", "data.sqlite")