import re

def clean(comment):
    
    # Supprimer la ponctuation
    comment = re.sub(r'[^\w\s]', '', comment)
    
    # Supprimer les URLs
    comment = re.sub(r'http\S+', '', comment)

    # Convertir en minuscules
    comment = comment.lower()

    return comment
