from target import ITarget


class Adapter(ITarget):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        print("Inside adapter and calling request method.")
        self.adaptee.specific_request()

