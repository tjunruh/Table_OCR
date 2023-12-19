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
            if self.number_of_digits(predictions[i]) > 1:
                if predictions[i].find('I') != -1:
                    predictions[i] = predictions[i].replace('I', '1')

                if predictions[i].find('S') != -1:
                    predictions[i] = predictions[i].replace('S', '5')

                if predictions[i].find('D') != -1:
                    predictions[i] = predictions[i].replace('D', '0')
                    
            elif self.number_of_letters(predictions[i]) > 1:
                predictions[i] = predictions[i].replace('5', 'S')
  
            if predictions[i] in string_set:
                predictions[i] = string_set[predictions[i]]
            elif ',' in predictions[i]:
                words = predictions[i].split(',')
                expanded_words = ''
                for j in range(len(words)):
                    if words[j] in string_set:
                        expanded_words = expanded_words + string_set[words[j]]
                    else:
                        expanded_words = expanded_words + words[j]

                    if j < (len(words) - 1):
                        expanded_words = expanded_words + ', ' 
                predictions[i] = expanded_words
            for key, value in char_set.items():
                if predictions[i].find(key) != -1:
                    predictions[i] = predictions[i].replace(key, value)

        predictions = self.expand_dashes(predictions)

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
        elif word.find(',') != -1:
            word = word.replace(', ', ',')
            words = []
            words = word.split(',')
            word = ''
            for w in words:
                if w in string_set:     
                    w = string_set[w]
                word = word + w + ', '
            word = word[:len(word)-2]

        for key, value in char_set.items():
            if word.find(key) != -1:
                word = word.replace(key, value)

        return word

    def number_of_digits(self, word):
        digits = 0
        for character in word:
            if character.isdigit():
                digits += 1
                
        return digits

    def number_of_letters(self, word):
        letters = 0
        for character in word:
            if not character.isdigit():
                letters += 1

        return letters
        
    def expand_dashes(self, predictions):
        rows_columns = []
        rows_columns = self.file_manager_operative.load_rows_columns()
        columns = int(rows_columns[1])
        for i in range(len(predictions)):
            if predictions[i] == '1' or predictions[i] == 'I':
                j = i - columns
                while j > 0:
                    cell_above = predictions[j]
                    if cell_above != '1' and cell_above != 'i':
                        predictions[i] = cell_above
                        break
                    j = j - columns
        return predictions
                
                
