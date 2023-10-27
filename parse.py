import pandas as pd
import json

def parse_excel(excel_filename, concepts_without_ids_filename):
    df = pd.read_excel(excel_filename)
    print(df.columns)

    list_of_concepts = []

    for index, row in df.iterrows():
        concept_dict = {}
        concept_dict['datasetCode'] = 'mat-test'
        concept_dict['domain'] = {
            "value": "MA",
            "origin": "lenoch"
        }

        definitions = []
        notes = []
        words = []
        conceptIds = []

        # definitions[]
        def create_definition(def_value, lang):
            return {
                "value": def_value,
                "lang": lang,
                "definitionTypeCode": "definitsioon"
            }

        # G	DEF ET 1	Eestikeelne definitsioon
        # H	DEF ET 2	Eestikeelne definitsioon

        et_defs = [row['DEF ET 1'], row['DEF ET 2']]
        et_defs = [definition for definition in et_defs if pd.notna(definition)]
        for definition in et_defs:
            definitions.append(create_definition(definition, "est"))

        # N	DEF EN 1	Ingliskeelne definitsioon
        # O	DEF EN 2	Ingliskeelne definitsioon

        en_defs = [row['DEF EN 1'], row['DEF EN 2']]
        en_defs = [definition for definition in en_defs if pd.notna(definition)]
        for definition in en_defs:
            definitions.append(create_definition(definition, "eng"))

        # U	DEF RU 1	Venekeelne definitsioon
        # V	DEF RU 2	Venekeelne definitsioon

        ru_defs = [row['DEF RU 1'], row['DEF RU 2']]
        ru_defs = [definition for definition in ru_defs if pd.notna(definition)]
        for definition in ru_defs:
            definitions.append(create_definition(definition, "rus"))

        # notes[]
        # W	NOTE 1	Mitteavalik mõiste märkus
        # Y	NOTE 2	Mitteavalik mõiste märkus

        if pd.notna([row['NOTE 1']]):
            notes.append(
                {
                    "value": row['NOTE 1'],
                    "lang": "est",
                    "publicity": False
                }
            )

        if pd.notna([row['NOTE 2']]):
            notes.append(
                {
                    "value": row['NOTE 2'],
                    "lang": "est",
                    "publicity": False
                }
            )

        # words[]

        def create_word(term, lang, lexemenote):
            word_dict = {
                "value": term.strip(),
                "lang": lang,
                "lexemePublicity": True
            }

            if pd.notna(lexemenote):
                word_dict["lexemeNotes"] = [lexemenote]

            return word_dict

        # B TERM ET 1   Eestikeelne termin	Kui väärtus puudub, siis ei salvestata midagi
        # C	TERM ET 2   Eestikeelne termin	Kui väärtus puudub, siis ei salvestata midagi
        # D	TERM ET 3   Eestikeelne termin	Kui väärtus puudub, siis ei salvestata midagi
        # E	TERM ET 4   Eestikeelne termin	Kui väärtus puudub, siis ei salvestata midagi

        et_terms = [row['TERM ET 1'], row['TERM ET 2'], row['TERM ET 3'], row['TERM ET 4']]
        et_terms = [term for term in et_terms if pd.notna(term)]
        for term in et_terms:
            words.append(create_word(term, "est", row['LEXEMENOTE ET'] if len(et_terms) == 1 else None))

        if len(et_terms) > 1 and pd.notna(row['LEXEMENOTE ET']):
            print(et_terms)
            if len(words) > 0:  # Check if 'words' list is not empty
                if "lexemeNotes" in words[0]:  # Check if 'lexemeNotes' already exists in the first word
                    words[0]["lexemeNotes"].append({"lang": "est", "value": row['LEXEMENOTE ET']})
                else:
                    words[0]["lexemeNotes"] = [{"lang": "est", "value": row['LEXEMENOTE ET']}]

        # J	TERM EN 1	Ingliskeelne termin
        # K	TERM EN 2	Ingliskeelne termin
        # L	TERM EN 3	Ingliskeelne termin
        # M	TERM EN 4	Ingliskeelne termin

        en_terms = [row['TERM EN 1'], row['TERM EN 2'], row['TERM EN 3']]
        en_terms = [term for term in en_terms if pd.notna(term)]

        for term in en_terms:
            words.append(create_word(term, "eng", None))

        # P	TERM RU 1	Venekeelne termin
        # Q	TERM RU 2	Venekeelne termin
        # R	TERM RU 3	Venekeelne termin

        ru_terms = [row['TERM RU 1'], row['TERM RU 2'], row['TERM RU 3']]
        ru_terms = [term for term in ru_terms if pd.notna(term)]

        for term in ru_terms:
            words.append(create_word(term, "rus", None))

        # conceptIds[]
        # A
        # Kui väärtus puudub, siis ei salvestata midagi

        if pd.notna(row['CONCEPT_ID']):
            conceptIds.append(row['CONCEPT_ID'])

        concept_dict['definitions'] = definitions
        concept_dict['notes'] = notes
        concept_dict['words'] = words
        concept_dict['conceptIds'] = conceptIds

        list_of_concepts.append(concept_dict)

    with open(concepts_without_ids_filename, "w", encoding='utf-8') as f:
        json.dump(list_of_concepts, f, ensure_ascii=False, indent=4)