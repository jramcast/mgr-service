from mgr.usecases.interfaces import FeaturesCache


class InMemoryFeaturesCache(FeaturesCache):

    def __init__(self):
        self.storage = {}

    def get(self, key: str):
        return self.storage.get(key)

    def set(self, key: str, entry):
        self.storage[key] = entry

    def __contains__(self, key: str) -> bool:
        return key in self.storage
