import pandas as pd
import json

# Read Excel file into DataFrame
df = pd.read_excel("Matemaatika 2022.xlsx")
print(df.columns)


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



    # Initialize the 'words' and 'notes' lists
    words = []
    notes = []
    definitions = []
    conceptIds = []

    if pd.notna(row['concept_id']):
        conceptIds.append(row['concept_id'])
    #     last_concept_id = row['concept_id']
    # concept_dict['concept_id'] = last_concept_id

    if pd.notna([row['mitteavalik note 1']]):
        notes.append(
            {
                "value": row['mitteavalik note 1'],
                "lang": "est",
                "publicity": False
            }
        )

    if pd.notna([row['mitteavalik note 2']]):
        notes.append(
            {
                "value": row['mitteavalik note 2'],
                "lang": "est",
                "publicity": False
            }
        )

    # Function to create word dictionaries
    def create_word(term, lang, lexemenote):
        word_dict = {
            "value": term.strip(),
            "lang": lang,
            "lexemePublicity": True
        }

        if pd.notna(lexemenote):
            word_dict["lexemeNotes"] = [lexemenote]

        return word_dict


    def create_definition(def_value, lang):
        return {
            "value": def_value,
            "lang": lang,
            "definitionTypeCode": "definitsioon"
        }

    # Handle Estonian definitions
    et_defs = [row['def (et)'], row['def (et).1']]
    et_defs = [definition for definition in et_defs if pd.notna(definition)]
    for definition in et_defs:
        definitions.append(create_definition(definition, "est"))

    # Handle English definitions
    en_defs = [row['def (en)']]
    en_defs = [definition for definition in en_defs if pd.notna(definition)]
    for definition in en_defs:
        definitions.append(create_definition(definition, "eng"))

    # Handle Russian definitions
    ru_defs = [row['def (ru)']]
    ru_defs = [definition for definition in ru_defs if pd.notna(definition)]
    for definition in ru_defs:
        definitions.append(create_definition(definition, "rus"))

    # Create a word dictionary for Estonian terms
    et_terms = [row['term (et)'], row['term (et) 1'], row['term (et) 2'], row['term (et) 3']]
    et_terms = [term for term in et_terms if pd.notna(term)]
    for term in et_terms:
        words.append(create_word(term, "est", row['lexemenote (et)'] if len(et_terms) == 1 else None))

    if len(et_terms) > 1 and pd.notna(row['lexemenote (et)']):
        print(et_terms)
        notes.append({"lang": "est", "value": row['lexemenote (et)']})

    # Create a word dictionary for English terms
    en_terms = [row['term (en) 1'], row['term (en) 2'], row['term (en) 3']]
    en_terms = [term for term in en_terms if pd.notna(term)]
    for term in en_terms:
        words.append(create_word(term, "eng", row['lexemenote (en)'] if len(en_terms) == 1 else None))

    if len(en_terms) > 1 and pd.notna(row['lexemenote (en)']):
        notes.append({"lang": "eng", "value": row['lexemenote (en)']})

    # Create a word dictionary for Russian terms
    ru_terms = [row['term (ru) 1'], row['term (ru) 2'], row['term (ru) 3']]
    ru_terms = [term for term in ru_terms if pd.notna(term)]
    for term in ru_terms:
        words.append(create_word(term, "rus", row['lexemenote (ru)'] if len(ru_terms) == 1 else None))

    if len(ru_terms) > 1 and pd.notna(row['lexemenote (ru)']):
        notes.append({"lang": "rus", "value": row['lexemenote (ru)']})

    concept_dict['definitions'] = definitions
    concept_dict['notes'] = notes
    concept_dict['words'] = words
    concept_dict['conceptIds'] = conceptIds

    # Add the dictionary to the list
    list_of_dicts.append(concept_dict)

# Save to JSON file
with open("output.json", "w", encoding='utf-8') as f:
    json.dump(list_of_dicts, f, ensure_ascii=False, indent=4)
