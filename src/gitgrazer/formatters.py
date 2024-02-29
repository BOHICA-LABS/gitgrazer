from pydantic import BaseModel
from typing import Any
from abc import ABC, abstractmethod


class CommitOutput(BaseModel):
    """
    CommitOutput

    A class representing the output of a commit.

    Attributes:
        commit_hash (str): The hash of the commit.
        author (str): The author of the commit.
        date (Any): The date of the commit.
        message (str): The message associated with the commit.

    """
    commit_hash: str
    author: str
    date: Any
    message: str

class CommitOutputFormatter(ABC):
    """
    This class defines an abstract base class for formatting commit information.

    """
    @abstractmethod
    def format(self, commit) -> str:
        pass

    def _build_output(self, commit) -> str:
        return str(self._generate_commit_output(commit))

    def _generate_commit_output(self, commit) -> CommitOutput:
        output = CommitOutput(
            commit_hash=commit.hexsha,
            author=commit.author.name,
            date=commit.authored_datetime,
            message=commit.message.strip(),
        )
        return output


    """def _build_output(self, commit):
        output = f"Commit Hash: {commit.hexsha}\n"
        output += f"Author: {commit.author.name}\n"
        output += f"Date: {commit.authored_datetime}\n"
        output += f"Message: {commit.message.strip()}\n"
        #if commit.parents:
        #    diff = commit.parents[0].diff(commit)
        #    change_description = self.generate_change_description(diff)
        #   output += f"\nChanges:\n{change_description}"
        return output
    """


class TextCommitOutputFormatter(CommitOutputFormatter):
    """
    Format the commit information into a text output.

    :param commit: The commit object to be formatted.
    :type commit: Commit
    :return: The formatted text output.
    :rtype: str
    """
    def format(self, commit):
        output = f"-" * 40 + "\n"
        output += self._build_output(commit)
        return output


class HTMLCommitOutputFormatter(CommitOutputFormatter):
    """
    Format the commit object as HTML.

    :param commit: Commit object to format as HTML.
    :type commit: Commit

    :return: HTML representation of the commit.
    :rtype: str
    """
    def format(self, commit):
        output = "<div class='commit'>\n"
        output += self._build_output(commit).replace("\n", "<br>")
        output += "</div>\n"
        return output


class CommitOutputFactory:
    """
    CommitOutputFactory

    This class represents a factory for creating instances of CommitOutputFormatter based on the output type.

    Methods:
        get_formatter(output_type: str) -> CommitOutputFormatter

    Attributes:
        None

    ---

    get_formatter(output_type: str) -> CommitOutputFormatter

    This method is used to get a CommitOutputFormatter instance based on the output type provided.

    Parameters:
        output_type (str): The type of output desired. Valid values are "text" for plain text formatting and "html" for HTML formatting.

    Returns:
        CommitOutputFormatter: An instance of the appropriate CommitOutputFormatter subclass based on the output type.

    Raises:
        ValueError: If the output_type provided is not valid.

    Example Usage:
        factory = CommitOutputFactory()
        formatter = factory.get_formatter("text")
        output = formatter.format(commit)
    """
    @staticmethod
    def get_formatter(output_type: str) -> CommitOutputFormatter:
        if output_type == "text":
            return TextCommitOutputFormatter()
        elif output_type == "html":
            return HTMLCommitOutputFormatter()
        else:
            raise ValueError("Invalid output type")
