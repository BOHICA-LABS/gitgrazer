from abc import ABC, abstractmethod
import datetime

class CommitFilter(ABC):
    @abstractmethod
    def is_match(self, commit) -> bool:
        pass

class AuthorFilter(CommitFilter):
    def __init__(self, author_name):
        self.author_name = author_name

    def is_match(self, commit):
        return commit.author.name == self.author_name

class DateFilter(CommitFilter):
    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date = start_date
        self.end_date = end_date

    def is_match(self, commit):
        commit_date = commit.authored_datetime.date()
        return self.start_date <= commit_date <= self.end_date

class MessageKeywordFilter(CommitFilter):
    def __init__(self, keywords):
        self.keywords = keywords

    def is_match(self, commit):
        message = commit.message.lower()  # Case-insensitive search
        return any(keyword in message for keyword in self.keywords)

class CommitObserver(ABC):
    @abstractmethod
    def on_commit_match(self, commit):
        pass

class CommitSearchManager:
    def __init__(self):
        self._filters = []
        self._observers = []

    def add_filter(self, commit_filter: CommitFilter):
        self._filters.append(commit_filter)

    def register_observer(self, observer: CommitObserver):
        self._observers.append(observer)

    def process_commits(self, commits):
        for commit in commits:
            if all(f.is_match(commit) for f in self._filters):
                for observer in self._observers:
                    observer.on_commit_match(commit)
                return True
        return False
