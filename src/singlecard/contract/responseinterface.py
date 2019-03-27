import abc


class SingleResponseInterface:

    __metaclass__ = abc.ABCMeta

    def respond(self):
        pass
