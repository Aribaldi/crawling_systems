import pickle
import unittest
from pathlib import Path
from module_3.indexing import get_texts, global_index
from module_3.search import search_wrapper


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.index_path = Path("../test_outputs/5_index.pickle")
        post = get_texts(5)
        all_items, documents = global_index(post, 5)
        with open(self.index_path, 'wb') as fp:
            pickle.dump(all_items, fp)
        return super().setUp()

    def test_search_single_entry(self):
        res = search_wrapper(self.index_path, "конференция", 5)
        expected = (1, [(2, 1)])
        self.assertTupleEqual(expected, res)

    def test_search_multiple_entry(self):
        res = search_wrapper(self.index_path, "профессор", 5)
        expected = (3, [(1, 2), (2, 1), (3, 2)])
        self.assertEqual(expected[0], res[0])
        self.assertEqual(expected[1], sorted(res[1]))

    def test_search_multiple_word_query(self):
        res = search_wrapper(self.index_path, "Ректор МГУ", 5)
        expected = (2, [(1, 2), (2, 2)])
        self.assertEqual(expected[0], res[0])
        self.assertEqual(expected[1], sorted(res[1]))

    def test_search_empty_query(self):
        self.assertRaises(TypeError, lambda: search_wrapper(self.index_path, "", 5))

    def test_search_out_of_vocabulary_word(self):
        self.assertRaises(TypeError, lambda: search_wrapper(self.index_path, "доцент", 5))




