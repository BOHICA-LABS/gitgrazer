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
    repository = git.Repo(REPOSITORY_PATH)
    commit_storage = JsonCommitDataStorage()
    description_strategy = BasicChangeDescriptionStrategy()
    search_manager = CommitSearchManager()
    search_manager.add_filter(AuthorFilter(SAMPLE_AUTHOR))
    output_format = CommitOutputFactory.get_formatter(TEXT_FORMAT)
    return repository, commit_storage, description_strategy, search_manager, output_format


def process_commits(commits, commit_storage, description_strategy, search_manager, output_format):
    for commit in commits[::-1]:
        if search_manager.process_commits([commit]):
            command = CommitCommand(commit, commit_storage, description_strategy)
            output = output_format.format(commit)
            print(output)


if __name__ == "__main__":
    repo, commit_storage, change_strategy, filter_manager, output_formatter = setup()
    commits = list(repo.iter_commits('main', max_count=MAX_COMMITS))
    process_commits(commits, commit_storage, change_strategy, filter_manager, output_formatter)
