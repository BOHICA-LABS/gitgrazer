from pydantic import BaseModel
from typing import Any

class CommitOutput(BaseModel):
    commit_hash: str
    author: str
    date: Any
    message: str
    change_description: str = None