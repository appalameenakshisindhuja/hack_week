from flask import Flask, request, jsonify
import json
import base64
import hashlib
import random
import time
from datetime import datetime
import re

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Global state for some endpoints
request_counter = 0
user_sessions = {}

@app.route('/api/echo', methods=['POST'])
def mysterious_echo():
    """
    This endpoint appears to be a simple echo, but has hidden behavior
    """
    global request_counter
    request_counter += 1
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Hidden behavior: reverses strings on every 3rd request
    if request_counter % 3 == 0:
        if isinstance(data.get('message'), str):
            data['message'] = data['message'][::-1]
    
    # Hidden behavior: adds timestamp on prime numbered requests
    if is_prime(request_counter):
        data['timestamp'] = datetime.now().isoformat()
    
    return jsonify(data)

@app.route('/api/transform', methods=['POST'])
def data_transformer():
    """
    Transforms data based on mysterious rules
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400
    
    text = data.get('input', '')
    
    # Hidden behavior: Different transformations based on input length
    length = len(text)
    
    if length < 5:
        # ROT13 for short inputs
        result = ''.join(chr((ord(c) - 97 + 13) % 26 + 97) if c.islower() 
                        else chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() 
                        else c for c in text)
    elif length < 15:
        # Base64 encode for medium inputs
        result = base64.b64encode(text.encode()).decode()
    elif length < 30:
        # Pig Latin for longer inputs
        words = text.split()
        result = ' '.join(word[1:] + word[0] + 'ay' if word and word[0] not in 'aeiou' 
                         else word + 'way' for word in words)
    else:
        # Hash for very long inputs
        result = hashlib.md5(text.encode()).hexdigest()
    
    return jsonify({
        "original": text,
        "transformed": result,
        "method": "classified"
    })

@app.route('/api/filter', methods=['POST'])
def content_filter():
    """
    Filters content based on hidden criteria
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No content to filter"}), 400
    
    content = data.get('content', '')
    filter_type = data.get('type', 'default')
    
    # Hidden behavior: Different filters based on type and content
    if filter_type == 'numbers':
        # Only keeps numbers
        result = ''.join(c for c in content if c.isdigit())
    elif filter_type == 'vowels':
        # Removes vowels
        result = ''.join(c for c in content if c.lower() not in 'aeiou')
    elif filter_type == 'reverse':
        # Keeps only consonants but reverses them
        consonants = ''.join(c for c in content if c.isalpha() and c.lower() not in 'aeiou')
        result = consonants[::-1]
    else:
        # Default: removes words with even length
        words = content.split()
        result = ' '.join(word for word in words if len(word) % 2 != 0)
    
    return jsonify({
        "original": content,
        "filtered": result,
        "characters_removed": len(content) - len(result)
    })

@app.route('/api/sequence', methods=['POST'])
def sequence_generator():
    """
    Generates sequences based on mysterious patterns
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing parameters"}), 400
    
    seed = data.get('seed', 1)
    count = data.get('count', 5)
    
    # Hidden behavior: Different sequences based on seed value
    if seed % 2 == 0:
        # Fibonacci for even seeds
        sequence = fibonacci_sequence(count, seed)
        pattern = "fibonacci_variant"
    elif seed % 3 == 0:
        # Powers of seed for multiples of 3
        sequence = [seed ** i for i in range(count)]
        pattern = "exponential"
    elif seed % 5 == 0:
        # Prime numbers starting from seed
        sequence = get_primes_from(seed, count)
        pattern = "primes"
    else:
        # Collatz-like sequence
        sequence = collatz_variant(seed, count)
        pattern = "chaotic"
    
    return jsonify({
        "sequence": sequence,
        "seed": seed,
        "count": count,
        "hint": f"Pattern detected: {len(pattern)} characters"
    })

@app.route('/api/memory', methods=['POST'])
def memory_bank():
    """
    Stores and retrieves data with mysterious behavior
    """
    global user_sessions
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    session_id = data.get('session', 'default')
    action = data.get('action', 'store')
    
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            'data': [],
            'access_count': 0,
            'creation_time': time.time()
        }
    
    session = user_sessions[session_id]
    session['access_count'] += 1
    
    if action == 'store':
        value = data.get('value')
        # Hidden behavior: corrupts data after 10 accesses
        if session['access_count'] > 10:
            if isinstance(value, str):
                value = ''.join(random.choice('!@#$%') if random.random() < 0.3 else c for c in value)
        
        session['data'].append({
            'value': value,
            'timestamp': time.time(),
            'corrupted': session['access_count'] > 10
        })
        
        return jsonify({
            "status": "stored",
            "session": session_id,
            "total_items": len(session['data']),
            "warnings": session['access_count']
        })
    
    elif action == 'retrieve':
        # Hidden behavior: randomly shuffles data after session gets old
        age = time.time() - session['creation_time']
        if age > 300:  # 5 minutes
            random.shuffle(session['data'])
        
        return jsonify({
            "data": session['data'],
            "session": session_id,
            "age_seconds": int(age),
            "integrity": "questionable" if age > 300 else "stable"
        })
    
    else:
        return jsonify({"error": "Unknown action"}), 400

@app.route('/api/validator', methods=['POST'])
def input_validator():
    """
    Validates input based on mysterious rules
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nothing to validate"}), 400
    
    value = data.get('value', '')
    validation_type = data.get('type', 'mystery')
    
    # Hidden behavior: Complex validation rules
    if validation_type == 'mystery':
        # Valid if: length is prime, contains both letters and numbers, starts with vowel
        length_valid = is_prime(len(value))
        mixed_valid = any(c.isalpha() for c in value) and any(c.isdigit() for c in value)
        vowel_start = value and value[0].lower() in 'aeiou'
        
        is_valid = length_valid and mixed_valid and vowel_start
        
        return jsonify({
            "valid": is_valid,
            "score": sum([length_valid, mixed_valid, vowel_start]),
            "criteria_met": {
                "length_prime": length_valid,
                "mixed_content": mixed_valid,
                "vowel_start": vowel_start
            }
        })
    
    elif validation_type == 'pattern':
        # Hidden regex pattern
        pattern = r'^[A-Z][a-z]+\d{2,4}[!@#]$'
        is_valid = bool(re.match(pattern, value))
        
        return jsonify({
            "valid": is_valid,
            "pattern_hint": "Capital start, lowercase middle, digits, special end",
            "example": "Hello123!" if not is_valid else "Pattern matched!"
        })
    
    else:
        return jsonify({"error": "Unknown validation type"}), 400

@app.route('/api/cipher', methods=['POST'])
def cipher_machine():
    """
    Encodes/decodes text with mysterious cipher
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No cipher data"}), 400
    
    text = data.get('text', '')
    operation = data.get('operation', 'encode')
    key = data.get('key', 0)
    
    # Hidden behavior: Different ciphers based on key value
    if key == 0:
        # Simple Caesar cipher
        shift = 3
        if operation == 'encode':
            result = caesar_cipher(text, shift)
        else:
            result = caesar_cipher(text, -shift)
    
    elif key % 7 == 0:
        # Atbash cipher (A=Z, B=Y, etc.)
        result = atbash_cipher(text)
    
    elif key % 4 == 0:
        # Reverse + ROT13
        if operation == 'encode':
            result = text[::-1]
            result = ''.join(chr((ord(c) - 97 + 13) % 26 + 97) if c.islower() 
                           else chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() 
                           else c for c in result)
        else:
            result = ''.join(chr((ord(c) - 97 + 13) % 26 + 97) if c.islower() 
                           else chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() 
                           else c for c in text)
            result = result[::-1]
    
    else:
        # XOR with key
        result = ''.join(chr(ord(c) ^ (key % 256)) for c in text)
    
    return jsonify({
        "result": result,
        "operation": operation,
        "key_type": get_key_type(key),
        "reversible": key != 0
    })

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci_sequence(count, start=1):
    if count <= 0:
        return []
    elif count == 1:
        return [start]
    
    sequence = [start, start]
    for _ in range(count - 2):
        sequence.append(sequence[-1] + sequence[-2])
    
    return sequence[:count]

def get_primes_from(start, count):
    primes = []
    candidate = max(start, 2)
    
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    
    return primes

def collatz_variant(start, count):
    sequence = [start]
    current = start
    
    for _ in range(count - 1):
        if current % 2 == 0:
            current = current // 2
        else:
            current = current * 3 + 1
        sequence.append(current)
    
    return sequence

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def atbash_cipher(text):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(ord('Z') - (ord(char) - ord('A')))
            else:
                result += chr(ord('z') - (ord(char) - ord('a')))
        else:
            result += char
    return result

def get_key_type(key):
    if key == 0:
        return "default"
    elif key % 7 == 0:
        return "reflection"
    elif key % 4 == 0:
        return "compound"
    else:
        return "numeric"

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    Returns API status and some hints
    """
    global request_counter, user_sessions
    
    return jsonify({
        "status": "operational",
        "total_requests": request_counter,
        "active_sessions": len(user_sessions),
        "endpoints": 7,
        "hint": "Not all behaviors are immediately obvious",
        "challenge": "Reverse engineer each endpoint's hidden logic"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)