import file_manager as fm

def short_to_long(predictions):
    shorthand = {}
    shorthand = fm.load_shorthand()
    for i in range(len(predictions)):
        if shorthand.has_key(predictions[i]):
            predictions[i] = shorthand[predictions[i]]

    return predictions
