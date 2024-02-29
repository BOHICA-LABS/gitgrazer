import git
from abc import ABC, abstractmethod
from storage import CommitDataStorage


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class ErrorHandlingCommandDecorator(Command):
    def __init__(self, wrapped_command: Command):
        self._wrapped_command = wrapped_command

    def execute(self):
        try:
            self._wrapped_command.execute()
        except Exception as e:
            print(f"Error occured during command execution: {e}")
            # You could potentially add logging or more sophisticated error handling here

class CommitCommand(Command):
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
