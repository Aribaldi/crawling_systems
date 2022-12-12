import pickle
import unittest
import numpy as np
from pathlib import Path
from module_3.indexing import get_texts, global_index
from module_3.zip_index import gamma_coding, gamma_decoding, zip_ind


class TestZipIndex(unittest.TestCase):
    def setUp(self) -> None:
        self.index_path = Path("../test_outputs/5_index.pickle")
        post = get_texts(5)
        all_items, documents = global_index(post, 5)
        with open(self.index_path, 'wb') as fp:
            pickle.dump(all_items, fp)
        return super().setUp()

    def test_gamma_encoding_decoding(self):
        input = np.array([1, 2, 1, 4])
        output = gamma_coding(input)
        expected = gamma_decoding(*output)
        self.assertListEqual(list(expected), list(input))

    def test_gamma_encoding_zero_input(self):
        input = np.array([0])
        self.assertRaises(ValueError, lambda: gamma_coding(input))

    def test_gamma_encoding_negative_input(self):
        input = np.array([-1])
        self.assertRaises(ValueError, lambda: gamma_coding(input))




