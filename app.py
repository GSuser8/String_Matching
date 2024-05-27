import csv
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)

def read_suggestions_from_csv(filename):
    suggestions = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                suggestions.extend(row)
    except FileNotFoundError:
        pass
    return suggestions

def write_suggestions_to_csv(filename, suggestion):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([suggestion])

suggestions_file = 'suggestions.csv'

class BloomFilter:
    def __init__(self, size, hash_functions):
        self.size = size
        self.hash_functions = hash_functions
        self.bit_array = [False] * size
        
    def add(self, item):
        for hash_func in self.hash_functions:
            index = hash_func(item) % self.size
            self.bit_array[index] = True
            
    def __contains__(self, item):
        for hash_func in self.hash_functions:
            index = hash_func(item) % self.size
            if not self.bit_array[index]:
                return False
        return True

def hash_function(text):
    return int(hashlib.sha256(text.encode()).hexdigest(), 16)

def xor_hash(s):
    hash_val = 0
    for char in s:
        hash_val ^= ord(char)
    return hash_val

def complex_modular_hash(s, base=257, modulus=int(1e9 + 9)):
    hash_val = 0
    for char in s:
        hash_val = hash_val * base + ord(char)
        hash_val ^= hash_val >> 10
        hash_val %= modulus
    return hash_val

def word_wise_rabin_karp(text, pattern):
    pattern_hash = (xor_hash(pattern), complex_modular_hash(pattern))
    pattern_length = len(pattern)
    hashes = {}
    words = text.split()
    for i, word in enumerate(words):
        word_hash = (xor_hash(word), complex_modular_hash(word))
        if word_hash == pattern_hash:
            if word == pattern:
                hashes[i] = word
    return hashes

bloom_filter = BloomFilter(10000, [hash_function, xor_hash, complex_modular_hash])

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.json.get('query')
        shouldappend = request.json.get('shouldappend')
        print(shouldappend)
        match = []
        suggestions = read_suggestions_from_csv(suggestions_file)
        for suggestion in suggestions:
            matches = word_wise_rabin_karp(suggestion.lower(), query.lower())
            if matches:
                match.append(suggestion)
        if shouldappend and query and query.lower() not in bloom_filter:
            bloom_filter.add(query.lower())
            write_suggestions_to_csv(suggestions_file, query)
            print("Inside shouldappend", shouldappend)
        return jsonify(match)
    elif request.method == 'GET':
        return "Enter the query in the request body."

if __name__ == '__main__':
    app.run(debug = True)