from file_manager import file_manager

class short_to_long:
    file_manager_operative = file_manager()

    def short_to_long(self, predictions):
        shorthand = {}
        shorthand = self.file_manager_operative.load_shorthand()
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

    def in_short(self, prediction):
        shorthand = {}
        shorthand = self.file_manager_operative.load_shorthand()
        if prediction in shorthand:
            return True
        else:
            return False

    def single_short_to_long(self, word):
        shorthand = {}
        shorthand = self.file_manager_operative.load_shorthand()
        char_set = {}
        string_set = {}
        for key, value in shorthand.items():
            if key.find('*') != -1:
                char_set[key.replace('*', '')] = value
            else:
                string_set[key] = value

        if word in string_set:
            word = string_set[word]
        for key, value in char_set.items():
            if word.find(key) != -1:
                word = word.replace(key, value)

        return word
        
