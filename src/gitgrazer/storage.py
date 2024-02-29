import json
import os
from abc import ABC, abstractmethod

class CommitDataStorage(ABC):
    @abstractmethod
    def save(self, commit_hash):
        pass

    @abstractmethod
    def has_commit(self, commit_hash):
        pass

class JsonCommitDataStorage(CommitDataStorage):
    def __init__(self, filepath='processed_commits.json'):
        self.filepath = filepath
        self._processed_commits = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                return set(json.load(file))
        return set()

    def save(self, commit_hash):
        self._processed_commits.add(commit_hash)
        with open(self.filepath, 'w') as file:
            json.dump(list(self._processed_commits), file)

    def has_commit(self, commit_hash):
        return commit_hash in self._processed_commits
