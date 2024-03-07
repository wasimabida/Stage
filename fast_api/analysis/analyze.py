from detoxify import Detoxify

def analyze_toxicity(comment):
    # Initialize the Detoxify model
    model = Detoxify('original')
    
    # Analyze toxicity of the comment
    results = model.predict(comment)

    return results

