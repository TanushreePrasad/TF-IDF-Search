# read the index.txt and prepare documents, vocab , idf

import os
import re

# Define the preprocess function
def preprocess(document_text):
    # remove the leading numbers from the string, remove not alpha numeric characters, make everything lowercase
    terms = [re.sub(r'[^a-zA-Z0-9]', '', term.lower()) for term in document_text.strip().split()[1:]]
    return terms

directory = 'C:\question scrapper\Qdata'
target_str = "Example 1:"

# Check if index.txt is present in the directory
index_file = os.path.join(directory, 'index.txt')
if os.path.isfile(index_file):
    # Process index.txt
    with open(index_file, 'r',encoding= 'utf-8-sig', errors = "ignore") as f:
        problem_statement = f.read()

    # Preprocess the problem statement
    #preprocessed_statement = preprocess(problem_statement)

    # Process the preprocessed statement as needed
    # ...
    # Your code for processing the preprocessed statement goes here
    # ...

    # Print the problem statement and its preprocessed version
    

# Iterate over the subdirectories in the directory
for subdirectory in os.listdir(directory):
    subdirectory_path = os.path.join(directory, subdirectory)
    if os.path.isdir(subdirectory_path):  # Check if the item is a directory
        print("Processing folder:", subdirectory)
        
        # Get the list of .txt files in the subdirectory
        txt_files = [file for file in os.listdir(subdirectory_path) if file.endswith('.txt')]
        
        # Iterate over the .txt files and read the contents
        for file in txt_files:
            file_path = os.path.join(subdirectory_path, file)
            with open(file_path, 'r', encoding= 'utf-8-sig', errors = "ignore") as f:
                problem_statement = f.read()

            # Preprocess the problem statement
            #preprocessed_statement = preprocess(problem_statement)

            # Process the preprocessed statement as needed
            # ...
            # Your code for processing the preprocessed statement goes here
            # ...

            # Print the problem statement and its preprocessed version
            
vocab = {}
documents = []
for index, line in enumerate(problem_statement):
    # read statement and add it to the line and then preprocess
    if target_str in line:
        break;
    else:
        tokens = preprocess(line)
        documents.append(tokens)
        tokens = set(tokens)
        for token in tokens:
            if token not in vocab:
                vocab[token] = 1
            else:
                vocab[token] += 1

# reverse sort the vocab by the values
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

print('Number of documents: ', len(documents))
print('Size of vocab: ', len(vocab))
print('Sample document: ', documents[0])

# save the vocab in a text file
with open('tf-idf/vocab.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

# save the idf values in a text file
with open('tf-idf/idf-values.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

# save the documents in a text file
with open('tf-idf/documents.txt', 'w') as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))


inverted_index = {}
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# save the inverted index in a text file
with open('tf-idf/inverted-index.txt', 'w') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))