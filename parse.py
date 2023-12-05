import pandas as pd
from dataclasses import asdict
from data_classes import Concept, Domain, Definition, Note, Word, Lexemenote
from collections import defaultdict
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
            datasetCode='ma-05-12',
            manualEventOn=None,
            manualEventBy=None,
            firstCreateEventOn=None,
            firstCreateEventBy=None,
            domains=[domain],
            definitions=definitions,
            notes=notes,
            forums=[],
            words=words,
            conceptIds=concept_ids
        )

        list_of_concepts.append(concept)

    # Serializing to JSON
    concepts_dict = [asdict(concept) for concept in list_of_concepts]
    with open(concepts_without_ids_filename, "w", encoding='utf-8') as f:
        json.dump(concepts_dict, f, ensure_ascii=False, indent=4)




def merge_concepts(concepts_filename_input, concepts_merged_filename):
    with open(concepts_filename_input, 'r', encoding='utf-8') as f:
        concepts = json.load(f)

    def get_word_set(words):
        return {word['value'].lower() for word in words}

    unique_concepts = defaultdict(list)

    for concept in concepts:
        words = concept['words']
        word_set = frozenset(get_word_set(words))
        unique_concepts[word_set].append(concept)

    merged_concepts = []

    for word_set, concepts_to_merge in unique_concepts.items():
        if len(concepts_to_merge) > 1:
            print(f"Merging concepts with words: {', '.join(word_set)}")
            merged_concept = concepts_to_merge[0].copy()

            for concept in concepts_to_merge[1:]:
                # Extend conceptIds
                merged_concept['conceptIds'].extend(concept['conceptIds'])

                # Merge definitions and notes
                merged_concept['definitions'].extend(concept.get('definitions', []))
                merged_concept['notes'].extend(concept.get('notes', []))

                # Merge lexemeNotes for each word
                for word in merged_concept['words']:
                    all_lexeme_notes = word.get('lexemeNotes', [])
                    for c in concepts_to_merge:
                        matching_words = [c_word for c_word in c['words'] if c_word['value'].lower() == word['value'].lower() and c_word['lang'] == word['lang']]
                        for mw in matching_words:
                            all_lexeme_notes.extend(mw.get('lexemeNotes', []))
                    word['lexemeNotes'] = all_lexeme_notes

                if concept['domains'] != merged_concept['domains']:
                    print(f"Conflict found when merging concepts with IDs {merged_concept['conceptIds']}: different domains")
            merged_concepts.append(merged_concept)
        else:
            merged_concepts.append(concepts_to_merge[0])

    with open(concepts_merged_filename, 'w', encoding='utf-8') as f:
        json.dump(merged_concepts, f, ensure_ascii=False, indent=4)

    return merged_concepts