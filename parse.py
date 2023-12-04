import pandas as pd
from dataclasses import asdict
from data_classes import Concept, Domain, Definition, Note, Word, Lexemenote
import json


def parse_excel(excel_filename, concepts_without_ids_filename):
    df = pd.read_excel(excel_filename)

    list_of_concepts = []

    for index, row in df.iterrows():
        # Domains
        domain = Domain(code="MA", origin="lenoch")

        # Definitions
        definitions = []
        for lang_code, lang in [("ET", "est"), ("EN", "eng"), ("RU", "rus")]:
            for i in range(1, 3):
                def_key = f"DEF {lang_code} {i}"
                if pd.notna(row[def_key]):
                    definitions.append(Definition(value=row[def_key], lang=lang, definitionTypeCode="definitsioon"))

        # Notes
        notes = []
        for note_index in range(1, 3):
            note_key = f"NOTE {note_index}"
            if pd.notna(row[note_key]):
                notes.append(Note(value=row[note_key], lang="est", publicity=False))

        # Words
        words = []
        for lang_code, lang in [("ET", "est"), ("EN", "eng"), ("RU", "rus")]:
            term_range = range(1, 4) if lang_code == "RU" else range(1, 5)

            terms = [row[f"TERM {lang_code} {i}"].strip() for i in term_range if pd.notna(row[f"TERM {lang_code} {i}"])]
            terms = [term for term in terms if term]  # This will filter out empty strings as well

            lexemenote = None
            if lang_code == "ET" and len(terms) == 1:
                lexemenote_value = row.get(f'LEXEMENOTE {lang_code}', None)
                if pd.notna(lexemenote_value):
                    lexemenote = Lexemenote(value=lexemenote_value.strip(), lang=lang, publicity=True)

            for term in terms:
                if term:  # Check if the term is not an empty string
                    word = Word(value=term, lang=lang, lexemePublicity=True)
                    if lexemenote:
                        word.lexemeNotes.append(lexemenote)
                    words.append(word)

        # Concept IDs
        concept_ids = []
        if pd.notna(row['CONCEPT_ID']):
            concept_ids.append(row['CONCEPT_ID'])

        # Creating Concept instance
        concept = Concept(
            datasetCode='mat-test',
            manualEventOn=None,  # Fill in appropriately if data is available
            manualEventBy=None,  # Fill in appropriately if data is available
            firstCreateEventOn=None,  # Fill in appropriately if data is available
            firstCreateEventBy=None,  # Fill in appropriately if data is available
            domains=[domain],
            definitions=definitions,
            notes=notes,
            forums=[],  # If you have forum data, process it similar to other fields
            words=words,
            conceptIds=concept_ids
        )

        list_of_concepts.append(concept)

    # Serializing to JSON
    concepts_dict = [asdict(concept) for concept in list_of_concepts]
    with open(concepts_without_ids_filename, "w", encoding='utf-8') as f:
        json.dump(concepts_dict, f, ensure_ascii=False, indent=4)