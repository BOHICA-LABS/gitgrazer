from abc import ABC, abstractmethod
import datetime

class CommitFilter(ABC):
    """
    Abstract base class for commit filters.

    The CommitFilter class defines the interface for implementing commit filters.

    """
    @abstractmethod
    def is_match(self, commit) -> bool:
        pass

class AuthorFilter(CommitFilter):
    """
    Represents a filter that checks if a commit's author name matches a given author name.

    :param author_name: The author name to filter for.
    :type author_name: str
    """
    def __init__(self, author_name):
        self.author_name = author_name

    def is_match(self, commit):
        return commit.author.name == self.author_name

class DateFilter(CommitFilter):
    """
    A filter used to match commits within a specific date range.

    :param start_date: The start date of the range.
    :type start_date: datetime.date
    :param end_date: The end date of the range.
    :type end_date: datetime.date
    """
    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date = start_date
        self.end_date = end_date

    def is_match(self, commit):
        commit_date = commit.authored_datetime.date()
        return self.start_date <= commit_date <= self.end_date

class MessageKeywordFilter(CommitFilter):
    """A filter that matches commits based on specific keywords in their commit messages.

    :param keywords: A list of keywords to search for in commit messages.
    :type keywords: list of str

    :inherits: CommitFilter

    Usage:
    >>> filter = MessageKeywordFilter(['bug', 'fix'])
    >>> commit = Commit('Fixed a bug in the login functionality')
    >>> filter.is_match(commit)
    True
    """
    def __init__(self, keywords):
        self.keywords = keywords

    def is_match(self, commit):
        message = commit.message.lower()  # Case-insensitive search
        return any(keyword in message for keyword in self.keywords)

class CommitObserver(ABC):
    """
    The `CommitObserver` class is an abstract base class that defines the interface for a commit observer.

    Any class that wants to observe commit events should inherit from this class and implement the `on_commit_match` method.

    Attributes:
        None

    .. seealso:: :class:`CommitMatcher`

    """
    @abstractmethod
    def on_commit_match(self, commit):
        pass

class CommitSearchManager:
    """
    The CommitSearchManager class is responsible for managing the search process for commits.

    :ivar _filters: A list of commit filters.
    :ivar _observers: A list of commit observers.

    """
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
