from abc import ABC, abstractmethod
from models import CommitOutput, ChangeDescription
import utils


class CommitOutputFormatter(ABC):
    """
    Abstract base class for commit output formatters.

    This class defines the interface for formatting commit output. Subclasses must implement the `format` method.

    """
    @abstractmethod
    def format(self, commit) -> str:
        pass

    def _build_output(self, commit) -> ChangeDescription:
        return utils.generate_commit_output(commit)


class TextCommitOutputFormatter(CommitOutputFormatter):
    """
    This class is a subclass of CommitOutputFormatter and provides a specific implementation for formatting commit outputs into text format. It includes a method called format, which takes
    * a CommitOutput object as input and returns a formatted string representation of the commit.

    Example usage:
        formatter = TextCommitOutputFormatter()
        commit_output = CommitOutput()
        # Set properties of commit_output
        formatted_output = formatter.format(commit_output)

    """
    SEPARATOR = "-" * 40

    def format(self, commit: CommitOutput) -> str:
        commit_output = self._build_output(commit)
        output_parts = [
            self.SEPARATOR,
            f"Commit Hash: {commit_output.commit_hash}",
            f"Author: {commit_output.author}",
            f"Date: {commit_output.date}",
            f"Message: {commit_output.message.strip()}",
            f"Diff Summary: {commit_output.diff_summary}"
            f"Changes: {commit_output.change_description}",

        ]
        formatted_output = "\n".join(output_parts)
        return formatted_output


class HTMLCommitOutputFormatter(CommitOutputFormatter):
    """
    Formats the commit information into an HTML string.

    :param commit: The commit information.
    :type commit: CommitOutput
    :return: The formatted HTML string.
    :rtype: str
    """
    def format(self, commit):
        commit_output = self._build_output(commit)
        sanitized_commit = self._sanitize_for_html(commit_output)
        output = f"<div class='commit'>\n{sanitized_commit}</div>\n"
        return output

    def _sanitize_for_html(self, commit_output: CommitOutput) -> str:
        commit_info = (
            f"Commit Hash: {commit_output.commit_hash}<br>"
            f"Author: {commit_output.author}<br>"
            f"Date: {commit_output.date}<br>"
            f"Message: {commit_output.message}<br>"
        )
        return utils.sanitize_for_html(commit_info)


class CommitOutputFactory:
    """
    CommitOutputFactory

    A factory class for creating CommitOutputFormatter objects based on the output type.

    Methods:
        create_formatter(output_type: str) -> CommitOutputFormatter
            Creates and returns a CommitOutputFormatter object based on the output type provided.

    """
    @staticmethod
    def create_formatter(output_type: str) -> CommitOutputFormatter:  # Renamed from get_formatter to create_formatter
        if output_type == "text":
            return TextCommitOutputFormatter()
        elif output_type == "html":
            return HTMLCommitOutputFormatter()
        else:
            raise ValueError("Invalid output type")

class CommitOutputFactory:
    """
    The `CommitOutputFactory` class provides a static method for getting the appropriate
    `CommitOutputFormatter` based on the output type.

    Attributes:
        None

    Methods:
        get_formatter: Gets the formatter for a given output type.

    Exceptions:
        ValueError: Raised when an invalid output type is provided.

    Usage:
        output_factory = CommitOutputFactory()
        output_formatter = output_factory.get_formatter("text")
    """
    @staticmethod
    def get_formatter(output_type: str) -> CommitOutputFormatter:
        if output_type == "text":
            return TextCommitOutputFormatter()
        elif output_type == "html":
            return HTMLCommitOutputFormatter()
        else:
            raise ValueError("Invalid output type")
