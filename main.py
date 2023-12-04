import parse
import import_requests


# Parse Excel
mat_excel = 'files/mat.xlsx'
concepts_without_ids = 'files/output.json'
concepts_with_ids = ''
parse.parse_excel(mat_excel, concepts_without_ids)

# Assign word IDs to words
#import_requests.update_word_ids(concepts_without_ids, 'eki', 'mat')

# Import concepts to Ekilex
#import_requests.import_concepts(concepts_with_ids, 'mat', 100000000)