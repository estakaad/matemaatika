import parse



# Parse Excel
mat_excel = 'files/mat.xlsx'
concepts_without_ids = 'files/output.json'

parse.parse_excel(mat_excel, concepts_without_ids)

# Assign word IDs to words

# Import concepts to Ekilex