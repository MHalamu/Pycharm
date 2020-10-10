from abc import ABCMeta, abstractmethod


class AnimalFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self):
        pass


class Animal(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        print "Sound of Dog."


class Cat(Animal):
    def make_sound(self):
        print "Sound of Cat."


class RandomFactory(AnimalFactory):

    def create(self):
        # check which animal to create
        return Dog()


class BalancedFactory(AnimalFactory):

    def check_no_of_animals(self):
        pass

    def create(self):
        # Check amount and pick animal with lowest quantity
        return Cat()


balanced_factory = BalancedFactory()
random_factory = RandomFactory()
list_of_animals = []

# code
# code
# code
# Here we want to create some animal but we don't know which
# Animal with the lower quantity
animal = balanced_factory.create()
list_of_animals.append(animal)
animal.make_sound()
# code
# code
# Here we want random animal
animal = random_factory.create()
list_of_animals.append(animal)
animal.make_sound()
