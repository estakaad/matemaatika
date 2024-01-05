import parse

# Parse Excel
mat_excel = 'files/matemaatika2023.xlsx'
concepts_without_ids = 'files/output.json'
concepts_merged = 'files/output_merged.json'
concepts_with_ids = ''

parse.parse_excel(mat_excel, concepts_without_ids)
parse.merge_concepts(concepts_without_ids, concepts_merged)
