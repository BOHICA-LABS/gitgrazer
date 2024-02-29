import json
import os
from abc import ABC, abstractmethod

class CommitDataStorage(ABC):
    """

    A class for storing commit data.

    """
    @abstractmethod
    def save(self, commit_hash):
        pass

    @abstractmethod
    def has_commit(self, commit_hash):
        pass

class JsonCommitDataStorage(CommitDataStorage):
    """
    This class is a implementation of the `CommitDataStorage` interface and provides functionality to store and retrieve processed commit data in a JSON file.

    :class: `JsonCommitDataStorage`

    Methods:
        - __init__(self, filepath='processed_commits.json'):
            Initializes a new instance of the `JsonCommitDataStorage` class.
            Parameters:
                - filepath (str): The path to the JSON file to be used for storage. If not provided, the default value is 'processed_commits.json'.

        - _load(self):
            Loads the processed commits from the JSON file.
            Returns:
                - set: A set of processed commit hashes.

        - save(self, commit_hash):
            Adds a commit hash to the list of processed commits and saves it to the JSON file.
            Parameters:
                - commit_hash (str): The commit hash to be added and saved.

        - has_commit(self, commit_hash):
            Checks if a commit hash is present in the processed commits.
            Parameters:
                - commit_hash (str): The commit hash to be checked.
            Returns:
                - bool: True if the commit hash is present, False otherwise.

    Example usage:
        storage = JsonCommitDataStorage('processed_commits.json')
        storage.save('commit_1')
        storage.save('commit_2')
        print(storage.has_commit('commit_1'))  # Output: True
        print(storage.has_commit('commit_3'))  # Output: False
    """
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
