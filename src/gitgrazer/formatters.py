from abc import ABC, abstractmethod
from models import CommitOutput
import utils


class CommitOutputFormatter(ABC):
    @abstractmethod
    def format(self, commit) -> str:
        pass

    def _build_output(self, commit) -> CommitOutput:
        return utils.generate_commit_output(commit)


class TextCommitOutputFormatter(CommitOutputFormatter):
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
