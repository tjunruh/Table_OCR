import file_manager as fm

def short_to_long(predictions):
    shorthand = {}
    shorthand = fm.load_shorthand()
    for i in range(len(predictions)):
        if predictions[i] in shorthand:
            predictions[i] = shorthand[predictions[i]]

    return predictions
