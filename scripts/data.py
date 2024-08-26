class PredictionStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictionStore, cls).__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def set_prediction(self, stage_name, value):
        self._data[stage_name] = value

    def get_prediction(self, stage_name):
        return self._data.get(stage_name, 0.0)
