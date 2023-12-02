# Import necessary libraries
import pandas as pd
import json

# Load table from a text file using pandas
table = pd.read_csv('AFINN-111.txt', sep='\t', header=None, names=['word', 'score'])

# Convert the pandas DataFrame to a dictionary with 'word' as keys and 'score' as values
afinn = dict(zip(table['word'], table['score']))

# Save the dictionary to a JSON file
with open('afinn111.json', 'w') as json_file:
    json.dump(afinn, json_file)

# Print the dictionary
print(afinn)
