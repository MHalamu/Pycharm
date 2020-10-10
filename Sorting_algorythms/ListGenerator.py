from abc import ABCMeta, abstractmethod
from random import shuffle
from enum import Enum



class ListTypes(Enum):
    ascending = 'ascending'
    descending = 'descending'
    random = 'random'
    v_shape = 'v_shape'
    a_shape = 'a_shape'
    constant = 'constant'


class AbstractListGenerator(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def generate(num_of_elements, start):
        pass


class AscendingList(AbstractListGenerator):
    @staticmethod
    def generate(num_of_elements, start=0):
        return [num for num in xrange(start, num_of_elements)]


class DescendingList(AbstractListGenerator):
    @staticmethod
    def generate(num_of_elements, start=0):
        return sorted([num for num in xrange(start, num_of_elements)],
                      reverse=True)


class RandomList(AbstractListGenerator):
    @staticmethod
    def generate(num_of_elements, start=0):
        list_to_shuffle = [num for num in xrange(start, num_of_elements)]
        shuffle(list_to_shuffle)
        return list_to_shuffle


class VShapeList(AbstractListGenerator):
    @staticmethod
    def generate(num_of_elements, start=0):
        low_half_list = sorted([num for num in xrange(start, num_of_elements / 2)],
                               reverse=True)
        high_half_list = [num for num in xrange(start, num_of_elements / 2)]
        return low_half_list + high_half_list


class AShapeList(AbstractListGenerator):
    @staticmethod
    def generate(num_of_elements, start=0):
        low_half_list = sorted([num for num in xrange(start, num_of_elements / 2)],
                               reverse=True)
        high_half_list = [num for num in xrange(start, num_of_elements / 2)]
        return high_half_list + low_half_list


class ConstantList(AbstractListGenerator):
    @staticmethod
    def generate(num_of_elements, start=0):
        return [1 for _ in xrange(start, num_of_elements)]


class ListGeneratorAbstractFactory(object):
    @staticmethod
    def create_list_generator(list_type):
        if list_type == ListTypes.ascending:
            return AscendingList()
        elif list_type == ListTypes.descending:
            return DescendingList()
        elif list_type == ListTypes.random:
            return RandomList()
        elif list_type == ListTypes.v_shape:
            return VShapeList()
        elif list_type == ListTypes.a_shape:
            return AShapeList()
        elif list_type == ListTypes.constant:
            return ConstantList()