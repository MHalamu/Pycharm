from abc import ABCMeta, abstractmethod, abstractproperty
import time
import unittest
from ListGenerator import ListGeneratorAbstractFactory, ListTypes
from enum import Enum
from copy import deepcopy
import math
import sys
sys.setrecursionlimit(27000)
from random import randint


class SortMethods(Enum):
    """Class stores methods available for sorting"""
    insertion_sort = 'insertion_sort'
    selection_sort = 'selection_sort'
    heap_sort = 'heap_sort'
    quick_sort = 'quick_sort'
    quick_sort_iter = 'quick_sort_iter'


class SortTimer(object):
    """Context manager for measuring time of specified operations"""
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.measurement = self.end - self.start



class AbstractSort(object):
    """Interface for sorting"""
    __metaclass__ = ABCMeta

    @abstractproperty
    def sorting_time(self):
        pass

    @abstractmethod
    def sort(self, list_to_sort):
        """Sort given list"""
        pass

    def show_sorting_time(self):
        """Common method for showing sorting time"""
        print "\t\t{0}: {1:.4f} s".format(self.__class__.__name__,
                                          self.sorting_time)


class InsertionSort(AbstractSort):
    # O(n) at best, O(n^2) at worst
    def __init__(self):
        self._sorting_time = None
        self.sorted_list = None

    @property
    def sorting_time(self):
        return self._sorting_time

    @sorting_time.setter
    def sorting_time(self, value):
        self._sorting_time = value

    def sort(self, list_to_sort):

        list_copy = deepcopy(list_to_sort)
        index_iterator = xrange(1, len(list_copy))
        self.x = 0
        with SortTimer() as sort_timer:
            for index in index_iterator:

                # prev_index will be decremented in a while loop to find position
                # to place actual_index_value.
                prev_index = index - 1

                prev_index_value = list_copy[prev_index]
                actual_index_value = list_copy[index]

                while prev_index >= 0 and prev_index_value > actual_index_value:
                    # new_index is being decremented from actual_index
                    # to the beginning of a list.
                    # Decrementing continues while the value is higher than
                    # on the actual_index.

                    # move values bigger than actual_index_value to right by 1 position
                    list_copy[prev_index+1] = prev_index_value

                    prev_index -= 1
                    prev_index_value = list_copy[prev_index]
                    self.x+=1
                if list_copy[prev_index + 1] != actual_index_value:
                    list_copy[prev_index+1] = actual_index_value
                    self.x+=1
        self._sorting_time = sort_timer.measurement
        self.sorted_list = list_copy
        print self.x

class SelectionSort(AbstractSort):
    # O(n^2) at best and worst
    def __init__(self):
        self._sorting_time = None
        self.sorted_list = None

    @property
    def sorting_time(self):
        return self._sorting_time

    @sorting_time.setter
    def sorting_time(self, value):
        self._sorting_time = value

    def sort(self, list_to_sort):
        list_copy = deepcopy(list_to_sort)
        with SortTimer() as sort_timer:
            self.x=0
            self.y=0
            for index in reversed(xrange(1, len(list_copy))):
                max_index = index
                for new_index in reversed(xrange(0, index)):
                    # Iterate through all elements (except those already sorted) to find one with maximum value
                    if list_copy[new_index] > list_copy[max_index]:
                        self.x+=1
                        max_index = new_index

                # Swap element on current index with max element
                list_copy[index], list_copy[max_index] = list_copy[max_index], list_copy[index]
                self.y+=1
        self.sorted_list = list_copy
        self._sorting_time = sort_timer.measurement
        print self.x, self.y

class HeapSort(AbstractSort):
    def __init__(self):
        self._sorting_time = None
        self.sorted_list = None

    @property
    def sorting_time(self):
        return self._sorting_time

    @sorting_time.setter
    def sorting_time(self, value):
        self._sorting_time = value

    def sort(self, list_to_sort):
        self.x=0
        list_copy = deepcopy(list_to_sort)
        #print "init list: %s" % list_copy

        with SortTimer() as sort_timer:
            self.build_heap(list_copy)

            list_size = len(list_copy)
            for index in reversed(xrange(1, list_size)):
                #print "list before swap %s" % list_copy
                list_copy[0], list_copy[index] = list_copy[index], list_copy[0]

                #print "list after swap: %s " % list_copy
                list_size -= 1
                self.heapify(list_copy, 0, list_size)
                #print "list after heapify: %s" % list_copy

        self.sorted_list = list_copy
        self._sorting_time = sort_timer.measurement
        print "heapsort: %s" % self.x
        #print "sorted list: %s" % list_copy

    def build_heap(self, num_list):
        heap_size = len(num_list)
        for parent_index in reversed(xrange(int(math.floor(heap_size / 2)))):
            self.heapify(num_list, parent_index, heap_size)

        #print "built heap: %s" % num_list

    def heapify(self, num_list, parent_index, heap_size):

        # Additional +1 to child1 and child2 because list indexing starts from 0
        child_index1 = (parent_index * 2) + 1
        child_index2 = (parent_index * 2) + 2
        self.x += 1
        if child_index1 < heap_size and num_list[child_index1] > num_list[parent_index]:
            max_value_index = child_index1
        else:
            max_value_index = parent_index

        if child_index2 < heap_size and num_list[child_index2] > num_list[max_value_index]:
            max_value_index = child_index2

        if max_value_index != parent_index:
            num_list[parent_index], num_list[max_value_index] = num_list[max_value_index],  num_list[parent_index]
            self.heapify(num_list, max_value_index, heap_size)
            print 'aa'


class QuickSort(AbstractSort):
    def __init__(self):
        self._sorting_time = None
        self.sorted_list = None

    @property
    def sorting_time(self):
        return self._sorting_time

    @sorting_time.setter
    def sorting_time(self, value):
        self._sorting_time = value

    def sort(self, list_to_sort):
        list_copy = deepcopy(list_to_sort)
        self.x = 0
        self.y = 0

        with SortTimer() as sort_timer:
            self.quick_sort(list_copy, 0, len(list_copy))

        self.sorted_list = list_copy
        self._sorting_time = sort_timer.measurement
        print "quicksort: %s" % self.x
        print self.y
    def quick_sort(self, list_to_sort, start_index, list_lenght):

        if start_index < list_lenght:

            stop_index = self.partition(list_to_sort, start_index, list_lenght)

            self.quick_sort(list_to_sort, start_index, stop_index)
            self.quick_sort(list_to_sort, stop_index+1, list_lenght)


    def partition(self, list_to_sort, start_index, list_length):
        x_index = int(math.floor((start_index+list_length-1)/2))
        x = list_to_sort[x_index]
        i = start_index
        j = list_length-1
        self.y+=1
        while True:
            while list_to_sort[j] > x:

                j -= 1
            while list_to_sort[i] < x:

                i += 1

            if i < j and list_to_sort[i] != list_to_sort[j]:
                list_to_sort[i], list_to_sort[j] = list_to_sort[j], list_to_sort[i]
                self.x += 1

            else:
                return j


class QuickSortIterative(AbstractSort):
    def __init__(self):
        self._sorting_time = None
        self.sorted_list = None

    @property
    def sorting_time(self):
        return self._sorting_time

    @sorting_time.setter
    def sorting_time(self, value):
        self._sorting_time = value

    def sort(self, list_to_sort):
        list_copy = deepcopy(list_to_sort)

        with SortTimer() as sort_timer:
            self.quick_sort(list_copy, 0, len(list_copy))

        self.sorted_list = list_copy
        self._sorting_time = sort_timer.measurement
        #print "sorted: %s" % self.sorted_list
    def quick_sort(self, list_to_sort, start_index, list_lenght):
        self.x=0
        stack = [start_index, list_lenght-1]

        while stack:
            h = stack.pop()
            l = stack.pop()

            p = self.partition(list_to_sort, l, h)
            if p-1 > l:
                stack.append(l)
                stack.append(p-1)

            if p+1 < h:
                stack.append(p+1)
                stack.append(h)

        print self.x
    def partition(self, list_to_sort, start_index, end_index):
        self.x+=1
        #x_index = int(math.floor((start_index + end_index) / 2))
        #x_index = end_index
        x_index = randint(start_index, end_index)
        x = list_to_sort[x_index]
        i = start_index
        j = end_index

        while True:
            while list_to_sort[j] > x:
                j -= 1
            while list_to_sort[i] < x:
                i += 1

            if i < j and list_to_sort[i] != list_to_sort[j]:
                list_to_sort[i], list_to_sort[j] = list_to_sort[j], list_to_sort[i]
            else:
                return j


class SortAbstractFactory(object):

    @staticmethod
    def create_sort(sort_type):
        if sort_type == SortMethods.insertion_sort:
            return InsertionSort()
        elif sort_type == SortMethods.selection_sort:
            return SelectionSort()
        elif sort_type == SortMethods.heap_sort:
            return HeapSort()
        elif sort_type == SortMethods.quick_sort:
            return QuickSort()
        elif sort_type == SortMethods.quick_sort_iter:
            return QuickSortIterative()


sort_methods_to_use = [#SortMethods.heap_sort,
                       #SortMethods.selection_sort,
                       #SortMethods.insertion_sort,
                       SortMethods.quick_sort,
                       #SortMethods.quick_sort_iter
                       ]

list_types_to_use = [#ListTypes.ascending,
                     #ListTypes.descending]
                     ListTypes.random,
                     ListTypes.v_shape,
                     #ListTypes.a_shape]
                     ListTypes.constant]


#
# for list_type in list_types_to_use:
#     list_generator = ListGeneratorAbstractFactory.create_list_generator(list_type)
#     print "\n----------------------------------"
#     print "List type: %s" % list_generator.__class__.__name__
#     print "----------------------------------"
#
#     for sort_method in sort_methods_to_use:
#         sort_algotyrhm_obj = SortAbstractFactory.create_sort(sort_method)
#         list_result = []
#         for n in xrange(5000, 5001, 5000):
#             #print "\n\tNumber of elements: %s" % n
#
#             list_to_sort_ = list_generator.generate(n)
#             sort_algotyrhm_obj.sort(list_to_sort_)
#             list_result.append(sort_algotyrhm_obj.sorting_time)
#
#         print "\t\t{0}: {1}".format(sort_algotyrhm_obj.__class__.__name__,
#                                     list_result)
#
#             #sort_algotyrhm_obj.show_sorting_time()
#
#             #list_to_sort_ = [1,9,3,3,3,6,7,2]
#             #list_to_sort_ = [1 for x in xrange(9000)]
#             #list_to_sort_ = [3,1,5,2,4]


# class MyTest(unittest.TestCase):
#     def test_insertion_sort(self):
#         sort_obj = InsertionSort()
#         sort_obj.sort([5, 3, 1, 2, 4])
#         self.assertEqual(sort_obj.sorted_list, [1, 2, 3, 4, 5])
#
#     def test_selection_sort(self):
#         sort_obj = SelectionSort()
#         sort_obj.sort([5, 3, 1, 2, 4])
#         self.assertEqual(sort_obj.sorted_list, [1, 2, 3, 4, 5])
#
#     def test_heap_sort(self):
#         sort_obj = HeapSort()
#         sort_obj.sort([5, 3, 1, 2, 4])
#         self.assertEqual(sort_obj.sorted_list, [1, 2, 3, 4, 5])
#
#     def test_quick_sort(self):
#         sort_obj = QuickSort()
#         sort_obj.sort([5, 3, 1, 2, 4])
#         self.assertEqual(sort_obj.sorted_list, [1, 2, 3, 4, 5])
#
# if __name__ == '__main__':
#     unittest.main()


sort_algotyrhm_obj = SortAbstractFactory.create_sort(SortMethods.quick_sort)
sort_algotyrhm_obj.sort([0,3,0,1])
print sort_algotyrhm_obj.sorted_list