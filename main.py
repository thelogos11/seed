from functions import generate_ontology, text_to_owl, run_reasoner, refine_ontology_with_feedback

def main():
    # Initial prompt to generate ontology
    prompt = "Generate an ontology for the financial domain including categories like Financial Instruments, Market Data, Corporate Actions, and Financial Statements."
    ontology_text = generate_ontology(prompt)
    
    # Convert text to OWL/RDF format
    ontology_graph = text_to_owl(ontology_text)
    
    # Run reasoner and get feedback
    feedback = run_reasoner(ontology_graph)
    
    # Template for refining ontology prompt
    prompt_template = "Refine the ontology considering the following feedback: {feedback}"
    
    # Feedback loop to refine ontology until consistent
    while feedback['status'] != 'consistent':
        refined_ontology_text = refine_ontology_with_feedback(feedback['details'], prompt_template)
        ontology_graph = text_to_owl(refined_ontology_text)
        feedback = run_reasoner(ontology_graph)
    
    print("Ontology is consistent and saved at 'ontologies/financial_ontology.owl'")

if __name__ == "__main__":
    main()
