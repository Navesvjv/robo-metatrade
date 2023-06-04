class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("New instanceee")
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
