from file_manager import file_manager
import itertools

class short_to_long:
    file_manager_operative = file_manager()
    dash_characters = ['V', 'W', 'Y']
    uncertain_characters = [['1', 'I'], ['5', 'S'], ['G', '6'], ['A', '4'], ['0', 'D', 'Q', 'U']]

    def short_to_long(self, predictions_input):
        predictions = predictions_input.copy()
        shorthand = {}
        shorthand = self.file_manager_operative.load_shorthand()
        char_set = {}
        string_set = {}
        common_entries = []
        common_entries = self.file_manager_operative.load_common_entries()
        
        for key, value in shorthand.items():
            if key.find('*') != -1:
                char_set[key.replace('*', '')] = value
            else:
                string_set[key] = value

        for i in range(len(predictions)):
            if predictions[i] in string_set.keys():
                predictions[i] = string_set[predictions[i]]
            elif ',' in predictions[i]:
                words = predictions[i].split(',')
                expanded_words = ''
                for j in range(len(words)):
                    if words[j] in string_set.keys():
                        expanded_words = expanded_words + string_set[words[j]]
                    elif words[j] in common_entries:
                        expanded_words = expanded_words + words[j]
                    else:
                        expanded_words = expanded_words + self.uncertainty_correction(words[j], string_set, common_entries)

                    if j < (len(words) - 1):
                        expanded_words = expanded_words + ', ' 
                predictions[i] = expanded_words
            elif (len(predictions[i]) > 0) and (predictions[i] not in common_entries):
                predictions[i] = self.uncertainty_correction(predictions[i], string_set, common_entries)
                predictions[i] = self.number_count_correction(predictions[i], 2);

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

    def single_short_to_long(self, word, column_above):
        shorthand = {}
        shorthand = self.file_manager_operative.load_shorthand()
        char_set = {}
        string_set = {}
        uppercase_word = word.upper()
        for key, value in shorthand.items():
            if key.find('*') != -1:
                char_set[key.replace('*', '')] = value
            else:
                string_set[key] = value

        if uppercase_word in string_set.keys():
            word = string_set[uppercase_word]
        elif word.find(',') != -1:
            word = word.replace(', ', ',')
            words = []
            words = word.split(',')
            word = ''
            for w in words:
                if w.upper() in string_set.keys():     
                    w = string_set[w.upper()]
                word = word + w + ', '
            word = word[:len(word)-2]
        elif uppercase_word in self.dash_characters:
            word = self.expand_dashes_single(uppercase_word, column_above)

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
            if predictions[i] in self.dash_characters:
                j = i - columns
                while j > 0:
                    cell_above = predictions[j]
                    if cell_above not in self.dash_characters:
                        predictions[i] = cell_above
                        break
                    j = j - columns
        return predictions

    def expand_dashes_single(self, word, column_above):
        if word in self.dash_characters:
            for entry in column_above[::-1]:
                if entry not in self.dash_characters:
                    word = entry
                    break
        return word

    def inverse_char_set(self, word):
        shorthand = {}
        shorthand = self.file_manager_operative.load_shorthand()
        char_set = {}
        for key, value in shorthand.items():
            if key.find('*') != -1:
                char_set[key.replace('*', '')] = value

        for key, value in char_set.items():
            if word.find(value) != -1:
                word = word.replace(value, key)

        return word

    def uncertainty_correction(self, prediction, shorthand, common_entries):
        uncertain_characters = []
        uncertain_characters_present = []
        prediction_copy = prediction
        for group in self.uncertain_characters:
            for character in group:
                if character in prediction_copy:
                    uncertain_characters.append(group)
                    uncertain_characters_present.append(character)
                    break
            
        all_combinations = list(itertools.product(*uncertain_characters))
        for i in range(len(uncertain_characters)):
            group = uncertain_characters[i]
            for j in range(len(group)):
                prediction_copy = prediction_copy.replace(group[j], uncertain_characters_present[i])
        last_iteration = uncertain_characters_present
        matches = []
        for i in range(len(all_combinations)):
            group = all_combinations[i]
            for j in range(len(group)):
                prediction_copy = prediction_copy.replace(last_iteration[j], group[j])
            if prediction_copy in shorthand:
                matches.append(shorthand[prediction_copy])
            elif prediction_copy in common_entries:
                matches.append(prediction_copy)
            last_iteration = group
        if len(matches) == 1:
            prediction = matches[0]
        return prediction

    def number_count_correction(self, prediction, number_count):
        if self.number_of_digits(prediction) >= number_count:
                prediction = prediction.replace('I', '1')
                prediction = prediction.replace('S', '5')
                prediction = prediction.replace('D', '0')
                prediction = prediction.replace('A', '4')
        return prediction

    def letter_count_correction(self, prediction, letter_count):
        if self.number_of_letters(prediction) >= letter_count:
                prediction = prediction.replace('5', 'S')
        return prediction
