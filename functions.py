from openai import OpenAI
from rdflib import Graph
import requests

MEMORY_PATH = 'memory/context.txt'
FEEDBACK_PATH = 'memory/feedback.txt'

client = OpenAI()

# Function to generate ontology using GPT
def generate_ontology(prompt, context=""):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{context}\n\n{prompt}"}
        ]
    )
    return completion.choices[0].message

# Function to convert text to OWL/RDF format
def text_to_owl(ontology_text):
    g = Graph()
    g.parse(data=ontology_text, format='turtle')
    return g

# Function to run reasoner and get feedback
def run_reasoner(ontology_graph, file_path='ontologies/financial_ontology.ttl'):
    ontology_graph.serialize(destination=file_path, format='turtle')
    # Assume reasoner API accepts OWL file and returns feedback
    response = requests.post("http://reasoner-api/validate", files={'file': open(file_path, 'rb')})
    return response.json()

# Function to refine ontology with feedback
def refine_ontology_with_feedback(feedback, previous_prompt):
    with open(FEEDBACK_PATH, 'a') as f:
        f.write(f"\n\nFeedback: {feedback}")
    
    with open(FEEDBACK_PATH, 'r') as f:
        feedback_context = f.read()
    
    refined_prompt = f"Refine the ontology generated from the following prompt considering the feedback provided:\n\nPrevious prompt: {previous_prompt}\n\nFeedback: {feedback_context}\n\nPlease generate a refined ontology in Turtle format."
    refined_ontology_text = generate_ontology(refined_prompt, context=feedback_context)
    
    # Summarize feedback to avoid exceeding token limit
    summarized_feedback = summarize_text(feedback_context)
    with open(FEEDBACK_PATH, 'w') as f:
        f.write(summarized_feedback)
    
    return refined_ontology_text

# Function to summarize text
def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text to retain key points:\n\n{text}"}
        ]
    )
    return response.choices[0].message['content']
