import unittest
from module_2.src.post import Post
from module_3.indexing import get_texts, single_doc_index, global_index


class TestIndexing(unittest.TestCase):

    def test_get_texts(self):
        texts = get_texts(5)
        param_list = (
            (1, 1, 1, 1670853483, 'Ректор СПбГУ предложил увеличить времы перерыва', 5, 4, 3, 2),
            (2, 1, 2, 1670864445, 'На конференции выступил профессор Иванов', 4, 5, 3, 2),
            (1, 2, 1, 1670864447, 'Ректор МГУ отстранил профессора Смирнова от занятий ', 5, 4, 3, 2),
            (2, 2, 2, 1670864439, 'Ректор МГУ предложил ректору СПбГУ поменяться местами', 5, 4, 3, 2),
            (3, 2, 3, 1670864475, 'Профессора кафедры АБВ потребовали увеличения числа занятий по практике',
             5, 4, 3, 2)
        )
        posts = [Post(*params) for params in param_list]

        self.assertListEqual(texts, posts)

    def test_single_doc_index(self):
        texts = get_texts(1)
        index = single_doc_index(texts[0])
        expected = {
            'ректор': {'1, 1': 1},
            'спбгу': {'1, 1': 1},
            'предложить': {'1, 1': 1},
            'увеличить': {'1, 1': 1},
            'врем': {'1, 1': 1},
            'перерыв': {'1, 1': 1}
        }
        items = {term: dict(counter) for term, counter in index.items().items()}
        self.assertDictEqual(expected, items)

    def test_global_index(self):
        texts = get_texts(5)
        expected = {
            'ректор': {'1, 1': 1, '1, 2': 1, '2, 2': 2},
            'спбгу': {'1, 1': 1, '2, 2': 1},
            'предложить': {'1, 1': 1, '2, 2': 1},
            'увеличить': {'1, 1': 1},
            'врем': {'1, 1': 1},
            'перерыв': {'1, 1': 1},
            'на': {'2, 1': 1},
            'конференция': {'2, 1': 1},
            'выступить': {'2, 1': 1},
            'профессор': {'2, 1': 1, '1, 2': 1, '3, 2': 1},
            'иванов': {'2, 1': 1},
            'мгу': {'1, 2': 1, '2, 2': 1},
            'отстранить': {'1, 2': 1},
            'смирнов': {'1, 2': 1},
            'от': {'1, 2': 1},
            'занятие': {'1, 2': 1, '3, 2': 1},
            'поменяться': {'2, 2': 1},
            'место': {'2, 2': 1},
            'кафедра': {'3, 2': 1},
            'абв': {'3, 2': 1},
            'потребовать': {'3, 2': 1},
            'увеличение': {'3, 2': 1},
            'число': {'3, 2': 1},
            'по': {'3, 2': 1},
            'практика': {'3, 2': 1}
        }
        index = global_index(texts, p_num=1)
        self.assertDictEqual(expected, index[0])

    def test_single_and_multiple_processes(self):
        texts = get_texts(5)
        index_single_process = global_index(texts, p_num=1)[0]
        index_multiple_process = global_index(texts, p_num=10)[0]
        self.assertDictEqual(index_single_process, index_multiple_process)







