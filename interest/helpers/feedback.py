class FeedbackList(list):

    # Public

    def __init__(self, feedback):
        self.__feedback = feedback

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__feedback()

    def __delitem__(self, key):
        super().__delitem__(key)
        self.__feedback()

    def append(self, obj):
        super().append(obj)
        self.__feedback()

    def insert(self, index, obj):
        super().insert(index, obj)
        self.__feedback()
