import hashlib
import time
import random
import string

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

def rabin_karp1(text, pattern):
    start_time = time.time()
    try:
        pattern_hash = (xor_hash(pattern), complex_modular_hash(pattern))
        pattern_length = len(pattern)
        matches = {}
        words = text.split()
        for i, word in enumerate(words):
            word_hash = (xor_hash(word), complex_modular_hash(word))
            if word_hash == pattern_hash and word == pattern:
                matches[i] = word
        execution_time = time.time() - start_time
        return matches, execution_time
    except Exception as e:
        print(f"Error in rabin_karp1: {e}")
        return {}, time.time() - start_time

class BloomFilter:
    def _init_(self, size, hash_functions):
        self.size = size
        self.hash_functions = hash_functions
        self.bit_array = [False] * size
        
    def add(self, item):
        for hash_func in self.hash_functions:
            index = hash_func(item) % self.size
            self.bit_array[index] = True
            
    def _contains_(self, item):
        for hash_func in self.hash_functions:
            index = hash_func(item) % self.size
            if not self.bit_array[index]:
                return False
        return True

def rabin_karp2(sentences, pattern):
    start_time = time.time()
    bloom_filter = BloomFilter(size=10000, hash_functions=[lambda x: int(hashlib.sha256(x.encode()).hexdigest(), 16)])
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            bloom_filter.add(word)
    
    result = pattern in bloom_filter
    execution_time = time.time() - start_time
    # return result, execution_time
    return {"matches": [pattern] if result else [], "execution_time": execution_time}

def precompute_hashes(text, pattern_length):
    hashes = {}
    for i in range(len(text) - pattern_length + 1):
        substring = text[i:i + pattern_length]
        hashes[substring] = hashlib.sha256(substring.encode()).hexdigest()
    return hashes

def rabin_karp3(text, pattern):
    start_time = time.time()
    pattern_length = len(pattern)
    pattern_hash = hashlib.sha256(pattern.encode()).hexdigest()
    precomputed_hashes = precompute_hashes(text, pattern_length)
    matches = []
    for i in range(len(text) - pattern_length + 1):
        substring = text[i:i + pattern_length]
        if precomputed_hashes.get(substring) == pattern_hash:
            if substring == pattern:
                matches.append(i)
    execution_time = time.time() - start_time
    return matches, execution_time

def rabin_karp4(text, pattern):
    start_time = time.time()
    n = len(text)
    m = len(pattern)
    pattern_sha256 = hashlib.sha256(pattern.encode()).hexdigest()
    matches = []
    for i in range(n - m + 1):
        text_substring_sha256 = hashlib.sha256(text[i:i + m].encode()).hexdigest()
        if text_substring_sha256 == pattern_sha256:
            if text[i:i + m] == pattern:
                matches.append(i)
    execution_time = time.time() - start_time
    return matches, execution_time

def calc_hash(s, prime=5, modulus=int(1e9 + 7)):
    hash_val = 0
    for i, char in enumerate(s):
        hash_val += ord(char) * (prime ** i)
        hash_val %= modulus
    return hash_val

def str_hash(old_hash, old_char, new_char, pattern_length, prime=5, modulus=int(1e9 + 7)):
    new_hash = old_hash - ord(old_char)
    new_hash /= prime
    new_hash = int(new_hash)
    new_hash += ord(new_char) * (prime ** (pattern_length - 1))
    new_hash %= modulus
    return new_hash

def rabin_karp5(text, pattern):
    start_time = time.time()
    pattern_length = len(pattern)
    str_hash_val = calc_hash(text[:pattern_length])
    pattern_hash = calc_hash(pattern)
    matches = []
    for i in range(len(text) - pattern_length + 1):
        if str_hash_val == pattern_hash and text[i:i + pattern_length] == pattern:
            matches.append(i)
        if i < len(text) - pattern_length:
            str_hash_val = str_hash(str_hash_val, text[i], text[i + pattern_length], pattern_length)
    execution_time = time.time() - start_time
    return matches, execution_time

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

import matplotlib.pyplot as plt

def measure_performance(algorithm, text, pattern):
    start_time = time.time()
    matches = algorithm(text, pattern)
    execution_time = time.time() - start_time
    return len(matches), execution_time

text = generate_random_string(100000)
pattern = generate_random_string(100)

variations = [rabin_karp1, rabin_karp2, rabin_karp3, rabin_karp4, rabin_karp5]
labels = ["RK1", "RK2", "RK3", "RK4", "RK5"]

results = {}
for label, variation in zip(labels, variations):
    matches_count, exec_time = measure_performance(variation, text, pattern)
    results[label] = {
        "execution_time": exec_time,
        "matches_count": matches_count
    }

for label, result in results.items():
    print(f"{label} - Execution Time: {result['execution_time']:.4f}s, Matches: {result['matches_count']}")

fig, ax = plt.subplots(2, 1, figsize=(10, 8))

ax[0].bar(results.keys(), [result["execution_time"] for result in results.values()], color='blue')
ax[0].set_title('Execution Time Comparison')
ax[0].set_ylabel('Execution Time (seconds)')

plt.tight_layout()
plt.show()