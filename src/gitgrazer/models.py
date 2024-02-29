from pydantic import BaseModel
from typing import Any


class CommitOutput(BaseModel):
    """
    Represents the output of a commit operation.

    Attributes:
        commit_hash (str): The hash of the commit.
        author (str): The name of the author of the commit.
        date (Any): The date of the commit.
        message (str): The commit message.
        change_description (str, optional): The description of the changes made in the commit.

    """
    commit_hash: str
    author: str
    date: Any
    message: str
    change_description: str = None
    diff_summary: str = None


class ChangeDescription(BaseModel):
    """
    ChangeDescription Class

    A class for representing a change description.

    Attributes:
        content (str): The content of the change description.
        diff_summary (str): A summary of the difference made by the change.

    """
    content: str
    diff_summary: str