import git
from abc import ABC, abstractmethod
from storage import CommitDataStorage


class Command(ABC):
    """

    The Command class is an abstract base class that provides a common interface for all command classes. It defines a single abstract method called `execute()`.

    Attributes:
        None

    Methods:
        - execute(): This method is an abstract method that needs to be implemented by subclasses. It represents the action that the command class should perform.

    Example usage:
        class MyCommand(Command):
            def execute(self):
                # Code to perform the command's action

            # Any additional methods or attributes specific to the MyCommand class can be defined here

    Note:
        This class is meant to be subclassed, not instantiated directly. Subclasses should provide an implementation for the `execute()` method.

    """
    @abstractmethod
    def execute(self):
        pass


class ErrorHandlingCommandDecorator(Command):
    """
    A decorator that provides error handling for a wrapped command.

    :param wrapped_command: The command to be wrapped.
    :type wrapped_command: Command
    """
    def __init__(self, wrapped_command: Command):
        self._wrapped_command = wrapped_command

    def execute(self):
        try:
            self._wrapped_command.execute()
        except Exception as e:
            print(f"Error occured during command execution: {e}")
            # You could potentially add logging or more sophisticated error handling here

class CommitCommand(Command):
    """

    CommitCommand

    This class represents a command for committing changes in a Git repository.

    Attributes:
        commit (Commit): The commit object to be processed.
        storage (CommitDataStorage): The data storage object used to store processed commits.
        change_strategy: The object responsible for generating change descriptions.

    Methods:
        execute(): Executes the command.

    """
    def __init__(self, commit, storage: CommitDataStorage, change_strategy):
        self.commit = commit
        self.storage = storage
        self.change_strategy = change_strategy

    def execute(self):
        if self.storage.has_commit(self.commit.hexsha):
            print(f"Commit {self.commit.hexsha} has already been processed.")
            return

        print("-" * 40)
        print("Commit Hash:", self.commit.hexsha)
        print("Author:", self.commit.author.name)
        print("Date:", self.commit.authored_datetime)
        print("Message:", self.commit.message.strip())

        if self.commit.parents:
            diff = self.commit.parents[0].diff(self.commit)
            change_description = self.change_strategy.generate(diff)
            print("\nChanges:\n", change_description)

        self.storage.save(self.commit.hexsha)

    # Example Usage: Adding Error Handling
#command = CommitCommand(commit, storage, strategy)
#decorated_command = ErrorHandlingCommandDecorator(command)
#decorated_command.execute()
