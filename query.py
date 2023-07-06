from flask import Flask, jsonify
import math
import re

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


def load_vocab():
    vocab = {}
    with open('tf-idf/vocab.txt', 'r') as f:
        vocab_terms = f.readlines()
    with open('tf-idf/idf-values.txt', 'r') as f:
        idf_values = f.readlines()
    
    for (term, idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open(r'C:\question scrapper\tf-idf\documents.txt', 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    # Load the question links
    with open(r'C:\question scrapper\Qdata\Qindex.txt', 'r') as f:
        question_links = f.readlines()
    question_links = [link.strip() for link in question_links]

    # Combine documents and question links
    combined_documents = []
    for i, document in enumerate(documents):
        if i < len(question_links):
            combined_document = {
                'document': document,
                'question_link': question_links[i]
            }
        else:
            combined_document = {
                'document': document,
                'question_link': ''
            }
        combined_documents.append(combined_document)

    print('Number of documents: ', len(combined_documents))
    print('Sample document: ', combined_documents[0])
    return combined_documents

def load_inverted_index():
    inverted_index = {}
    with open('tf-idf/inverted-index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0, len(inverted_index_terms), 2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    print('Size of inverted index: ', len(inverted_index))
    return inverted_index

vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()

def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values

def get_idf_value(term):
    return math.log(len(documents) / vocab_idf_values[term])

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    results = []

    for term in query_terms:
        if vocab_idf_values[term] == 0:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            potential_documents[document] += tf_values_by_document[document] * idf_value

    # Divide by the length of the query terms
    for document_index in potential_documents:
        document = documents[int(document_index)]
        question_link = document['question_link']
        score = potential_documents[document_index]
        results.append({
            'Document': document,
            'Question Link': question_link,
            'Score': score
        })

    return results


results = calculate_sorted_order_of_documents(query_terms)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Tanushree'

class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')

@app.route("/<query>")
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(calculate_sorted_order_of_documents(q_terms)[:20:]) 

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results = calculate_sorted_order_of_documents(q_terms)[:20:]
    return render_template('index.html', form=form, results=results)   
