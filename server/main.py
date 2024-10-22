# # from flask import Flask, request, jsonify
# # from transformers import pipeline
# # import time
# # # import CORS

# # app = Flask(__name__)

# # # Global variable to store the model
# # MODEL = None

# # def load_model():
# #     """Load the zero-shot classification model at startup"""
# #     global MODEL
# #     print("Loading model...")
# #     MODEL = pipeline(
# #         "zero-shot-classification",
# #        model="cross-encoder/nli-distilroberta-base",
# #         device=-1  # Run on CPU
# #     )
# #     print("Model loaded successfully!")

# # def is_legal_topic(prompt):
# #     """
# #     Use zero-shot classification to determine if the prompt is legal-related
# #     """
# #     candidate_labels = [
# #         "legal advice",
# #         "law",
# #         "court proceedings",
# #         "general conversation",
# #         "casual topics"
# #     ]
    
# #     # Get classification results
# #     results = MODEL(
# #         prompt,
# #         candidate_labels=candidate_labels,
# #         multi_label=False
# #     )
    
# #     # Check if top prediction is legal-related
# #     top_label = results['labels'][0]
# #     top_score = results['scores'][0]
    
# #     # Consider it legal if the top prediction is one of the legal categories
# #     # and the confidence score is above 0.5
# #     legal_categories = {"legal advice", "law", "court proceedings"}
# #     is_legal = top_label in legal_categories and top_score > 0.5
    
# #     return {
# #         'is_legal': is_legal,
# #         'top_label': top_label,
# #         'confidence': top_score
# #     }

# # def generate_response(prompt):
# #     """
# #     Dummy function to generate response
# #     """
# #     return f"This is a dummy response to: {prompt}"

# # @app.route('/process_prompt', methods=['POST'])
# # def process_prompt():
# #     try:
# #         data = request.get_json()
        
# #         if not data or 'prompt' not in data:
# #             return jsonify({
# #                 'error': 'No prompt provided'
# #             }), 400

# #         prompt = data['prompt']
        
# #         # Check if it's a legal topic with the model
# #         classification_result = is_legal_topic(prompt)
        
# #         # Generate response if it's not a legal topic
# #         if not classification_result['is_legal']:
# #             response = generate_response(prompt)
            
# #             return jsonify({
# #                 'response': response,
# #                 'classification': classification_result
# #             })
# #         else:
# #             return jsonify({
# #                 'response': 'Cannot process legal-related queries',
# #                 'classification': classification_result
# #             })

# #     except Exception as e:
# #         return jsonify({
# #             'error': str(e)
# #         }), 500

# # if __name__ == '__main__':
# #     # Load the model before starting the server
# #     load_model()
# #     # cors = CORS(app)
# #     # Start the Flask server
# #     app.run(debug=True, host='0.0.0.0', port=5000)

# from flask import Flask, request, jsonify
# from transformers import pipeline
# import time
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Global variables to store both models
# CLASSIFIER_MODEL = None
# RESPONSE_MODEL = None

# def load_models():
#     """Load both models at startup"""
#     global CLASSIFIER_MODEL, RESPONSE_MODEL
    
#     print("Loading classifier model...")
#     CLASSIFIER_MODEL = pipeline(
#         "zero-shot-classification",
#         model="cross-encoder/nli-distilroberta-base",
#         device=-1  # Run on CPU
#     )
#     print("Classifier model loaded successfully!")
    
#     print("Loading response model...")
#     # Using a small GPT-2 model for text generation
#     RESPONSE_MODEL = pipeline(
#         "text-generation",
#         model="distilgpt2",  # Much smaller than full GPT-2
#         device=-1  # Run on CPU
#     )
#     print("Response model loaded successfully!")

# def is_legal_topic(prompt):
#     """
#     Use lightweight model to determine if the prompt is legal-related
#     """
#     candidate_labels = [
#         "legal topic",
#         "general conversation"
#     ]
    
#     results = CLASSIFIER_MODEL(
#         prompt,
#         candidate_labels=candidate_labels,
#         multi_label=False
#     )
    
#     top_label = results['labels'][0]
#     top_score = results['scores'][0]
    
#     return {
#         'is_legal': top_label == "legal topic" and top_score > 0.5,
#         'top_label': top_label,
#         'confidence': top_score
#     }

# def generate_response(prompt):
#     """
#     Generate response using the response model
#     """
#     # Add a prefix to help guide the model's response
#     prefixed_prompt = f"Q: {prompt}\nA:"
    
#     # Generate response with reasonable parameters
#     response = RESPONSE_MODEL(
#         prefixed_prompt,
#         max_length=100,
#         num_return_sequences=1,
#         temperature=0.7,
#         pad_token_id=50256  # EOS token for GPT-2
#     )
    
#     # Clean up the generated text
#     generated_text = response[0]['generated_text']
#     # Extract just the answer part (after "A:")
#     answer = generated_text.split("A:")[-1].strip()
    
#     return answer

# @app.route('/process_prompt', methods=['POST'])
# def process_prompt():
#     try:
#         data = request.get_json()
        
#         if not data or 'prompt' not in data:
#             return jsonify({
#                 'error': 'No prompt provided'
#             }), 400

#         prompt = data['prompt']
        
#         # First, check if it's a legal topic
#         classification_result = is_legal_topic(prompt)
        
#         # Generate response if it's not a legal topic
#         if not classification_result['is_legal']:
#             response = generate_response(prompt)
            
#             return jsonify({
#                 'response': response,
#                 'classification': classification_result
#             })
#         else:
#             return jsonify({
#                 'response': 'Cannot process legal-related queries',
#                 'classification': classification_result
#             })

#     except Exception as e:
#         return jsonify({
#             'error': str(e)
#         }), 500

# if __name__ == '__main__':
#     # Load both models before starting the server
#     load_models()
#     # Start the Flask server
#     app.run(debug=True, host='0.0.0.0', port=5000)


#####failed try

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import time
import uuid
import os

app = Flask(__name__)
CORS(app)

# Global variables for models
CLASSIFIER_MODEL = None
RESPONSE_MODEL = None
EMBEDDING_MODEL = None
VECTOR_DB = None
COLLECTION = None

def load_models():
    """Load all models at startup"""
    global CLASSIFIER_MODEL, RESPONSE_MODEL, EMBEDDING_MODEL, VECTOR_DB, COLLECTION
    
    print("Loading classifier model...")
    CLASSIFIER_MODEL = pipeline(
        "zero-shot-classification",
        model="cross-encoder/nli-distilroberta-base",
        device=-1
    )
    
    print("Loading response model...")
    RESPONSE_MODEL = pipeline(
        "text-generation",
        model="distilgpt2",
        device=-1
    )
    
    print("Loading embedding model...")
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')  # Small but effective model
    
    print("Initializing ChromaDB...")
    VECTOR_DB = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="db"
    ))
    
    # Create or get the collection
    COLLECTION = VECTOR_DB.get_or_create_collection(
        name="document_chunks",
        metadata={"hnsw:space": "cosine"}
    )
    
    print("All models and DB loaded successfully!")

def process_document(text):
    """Split document into chunks and return with embeddings"""
    # Simple chunking by sentences (you might want to use a more sophisticated approach)
    chunks = [s.strip() for s in text.split('.') if len(s.strip()) > 0]
    
    # Generate embeddings for chunks
    embeddings = EMBEDDING_MODEL.encode(chunks).tolist()
    
    # Generate unique IDs for each chunk
    ids = [str(uuid.uuid4()) for _ in chunks]
    
    return chunks, embeddings, ids

def is_legal_topic(prompt):
    """Use lightweight model to determine if the prompt is legal-related"""
    candidate_labels = [
        "legal topic",
        "general conversation"
    ]
    
    results = CLASSIFIER_MODEL(
        prompt,
        candidate_labels=candidate_labels,
        multi_label=False
    )
    
    top_label = results['labels'][0]
    top_score = results['scores'][0]
    
    return {
        'is_legal': top_label == "legal topic" and top_score > 0.5,
        'top_label': top_label,
        'confidence': top_score
    }

def generate_response(prompt):
    """Generate response using the response model"""
    prefixed_prompt = f"Q: {prompt}\nA:"
    
    response = RESPONSE_MODEL(
        prefixed_prompt,
        max_length=100,
        num_return_sequences=1,
        temperature=0.7,
        pad_token_id=50256
    )
    
    generated_text = response[0]['generated_text']
    answer = generated_text.split("A:")[-1].strip()
    
    return answer

def find_similar_chunks(query, n_results=3):
    """Find similar text chunks for a given query"""
    # Generate embedding for the query
    query_embedding = EMBEDDING_MODEL.encode(query).tolist()
    
    # Search in the collection
    results = COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results

@app.route('/upload_document', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read and process the document
        text = file.read().decode('utf-8')
        chunks, embeddings, ids = process_document(text)
        
        # Add to ChromaDB
        COLLECTION.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids
        )
        
        return jsonify({
            'message': 'Document processed successfully',
            'chunks_added': len(chunks)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400

        prompt = data['prompt']
        
        # First, check if it's a legal topic
        classification_result = is_legal_topic(prompt)
        
        if not classification_result['is_legal']:
            # Find similar content in the database
            similar_chunks = find_similar_chunks(prompt)
            
            # Generate response
            response = generate_response(prompt)
            
            return jsonify({
                'response': response,
                'classification': classification_result,
                'similar_chunks': similar_chunks
            })
        else:
            return jsonify({
                'response': 'Cannot process legal-related queries',
                'classification': classification_result
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000)