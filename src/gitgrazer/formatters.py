from pydantic import BaseModel
from typing import Any
from abc import ABC, abstractmethod


class CommitOutput(BaseModel):
    commit_hash: str
    author: str
    date: Any
    message: str

class CommitOutputFormatter(ABC):
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
    def format(self, commit):
        output = f"-" * 40 + "\n"
        output += self._build_output(commit)
        return output


class HTMLCommitOutputFormatter(CommitOutputFormatter):
    def format(self, commit):
        output = "<div class='commit'>\n"
        output += self._build_output(commit).replace("\n", "<br>")
        output += "</div>\n"
        return output


class CommitOutputFactory:
    @staticmethod
    def get_formatter(output_type: str) -> CommitOutputFormatter:
        if output_type == "text":
            return TextCommitOutputFormatter()
        elif output_type == "html":
            return HTMLCommitOutputFormatter()
        else:
            raise ValueError("Invalid output type")
