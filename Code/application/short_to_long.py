import file_manager as fm

def short_to_long(predictions):
    shorthand = {}
    shorthand = fm.load_shorthand()
    char_set = {}
    string_set = {}
    for key, value in shorthand.items():
        if key.find('*') != -1:
            char_set[key.replace('*', '')] = value
        else:
            string_set[key] = value

    for i in range(len(predictions)):
        if predictions[i] in string_set:
            predictions[i] = string_set[predictions[i]]
        for key, value in char_set.items():
            if predictions[i].find(key) != -1:
                predictions[i] = predictions[i].replace(key, value)

    return predictions

def in_short(prediction):
    shorthand = {}
    shorthand = fm.load_shorthand()
    if prediction in shorthand:
        return True
    else:
        return False
