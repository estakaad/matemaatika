import pandas as pd
import json

# Read Excel file into DataFrame
df = pd.read_excel("Matemaatika 2022.xlsx")

# Initialize list to store dictionaries
list_of_dicts = []

# Initialize variable to store the last non-empty concept_id
last_concept_id = None

# Loop through each row in DataFrame
for index, row in df.iterrows():
    concept_dict = {}
    concept_dict['datasetCode'] = 'mat'
    concept_dict['domain'] = {
        "value": "MA",
        "origin": "lenoch"
    }

    if pd.notna(row['concept_id']):
        last_concept_id = row['concept_id']
    concept_dict['concept_id'] = last_concept_id

    # Initialize the 'words' and 'notes' list
    words = []
    notes = []

    # Function to create word dictionaries
    def create_word(term, lang, lexemenote):
        return {
            "value": term,
            "lang": lang,
            "lexemeValueStateCode": None,
            "lexemePublicity": True,
            "wordTypeCodes": [],
            "usages": [],
            "lexemeNotes": [lexemenote] if pd.notna(lexemenote) else [],
            "lexemeSourceLinks": []
        }

    # Create a word dictionary for Estonian terms
    et_terms = [row['term (et)'], row['term (et) 1'], row['term (et) 2']]
    et_terms = [term for term in et_terms if pd.notna(term)]
    for term in et_terms:
        words.append(create_word(term, "est", row['lexemenote (et)'] if len(et_terms) == 1 else None))

    if len(et_terms) > 1 and pd.notna(row['lexemenote (et)']):
        notes.append({"lang": "est", "value": row['lexemenote (et)']})

    # Repeat similar blocks for English and Russian terms
    # ...

    # Add 'words' and 'notes' to the concept dictionary
    concept_dict['words'] = words
    concept_dict['notes'] = notes

    # Add the dictionary to the list
    list_of_dicts.append(concept_dict)

# Save to JSON file
with open("output.json", "w", encoding='utf-8') as f:
    json.dump(list_of_dicts, f, ensure_ascii=False, indent=4)
