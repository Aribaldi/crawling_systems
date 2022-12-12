import unittest
from module_3.preprocessing import remove_punct, tokenize, lemmatize, clean


class TestPreprocessing(unittest.TestCase):

    def test_cyrillic_alphabet(self):
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.assertEqual(remove_punct(alphabet), alphabet)

    def test_latin_alphabet(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"
        self.assertEqual(remove_punct(alphabet), "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz")

    def test_digits(self):
        string = "1234567890 123 4567 89012"
        self.assertEqual(remove_punct(string), string)

    def test_punctuation(self):
        string = "!@#$%^&*!;:()[]{}`~,.?"
        self.assertEqual(remove_punct(string), "                      ")

    def test_trimming_text(self):
        query = '        ректор спбгу           \n'
        preprocessed = clean(query)
        self.assertEqual(preprocessed, ['ректор', 'спбгу'])

    def test_lowercase_transition(self):
        query = 'РЕКТОР СПБГУ'
        preprocessed = clean(query)
        self.assertEqual(preprocessed, ['ректор', 'спбгу'])

    def test_space_symbols_removal(self):
        query = '\n\rректор\nмгу\t\n'
        preprocessed = clean(query)
        self.assertEqual(preprocessed, ['ректор', 'мгу'])

    def test_multiple_spaces_replacing(self):
        query = 'ректором            мгу'
        preprocessed = clean(query)
        self.assertEqual(preprocessed, ['ректор', 'мгу'])
