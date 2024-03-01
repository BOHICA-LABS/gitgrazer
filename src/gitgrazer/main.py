import git
from commands import CommitCommand
from storage import JsonCommitDataStorage
from strategies import BasicChangeDescriptionStrategy
from filters import CommitSearchManager, AuthorFilter
from formatters import CommitOutputFactory, TextCommitOutputFormatter

TEXT_FORMAT = "text"
SAMPLE_AUTHOR = "Joshua Magady"
REPOSITORY_PATH = '../../'
MAX_COMMITS = 10


def setup():
    """
    Setup the necessary components for the method to execute.

    :return: a tuple containing:
        - repository: An instance of the git.Repo class representing the repository at the specified path.
        - commit_storage: An instance of the JsonCommitDataStorage class.
        - description_strategy: An instance of the BasicChangeDescriptionStrategy class.
        - search_manager: An instance of the CommitSearchManager class.
        - output_format: An instance of the formatter object from the CommitOutputFactory.get_formatter method.
    """
    repository = git.Repo(REPOSITORY_PATH)
    commit_storage = JsonCommitDataStorage()
    description_strategy = BasicChangeDescriptionStrategy()
    search_manager = CommitSearchManager()
    search_manager.add_filter(AuthorFilter(SAMPLE_AUTHOR))
    output_format = CommitOutputFactory.get_formatter(TEXT_FORMAT)
    return repository, commit_storage, description_strategy, search_manager, output_format


def process_commits(commits, commit_storage, description_strategy, search_manager, output_format):
    """
    Process commits in reverse order.


    :param commits: List of commits to process.
    :param commit_storage: Object representing commit storage.
    :param description_strategy: Object representing description strategy.
    :param search_manager: Object representing search manager.
    :param output_format: Output format for each commit.
    :return: None
    """
    for commit in commits[::-1]:
        if search_manager.process_commits([commit]):
            command = CommitCommand(commit, commit_storage, description_strategy)
            command.execute()
            output = output_format.format(commit)
            print(output)


if __name__ == "__main__":
    repo, commit_storage, change_strategy, filter_manager, output_formatter = setup()
    commits = list(repo.iter_commits('main', max_count=MAX_COMMITS))
    process_commits(commits, commit_storage, change_strategy, filter_manager, output_formatter)
