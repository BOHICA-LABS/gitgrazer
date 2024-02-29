from abc import ABC, abstractmethod

class ChangeDescriptionStrategy(ABC):
    """

    ChangeDescriptionStrategy

    Abstract base class representing a strategy for generating change descriptions.

    """
    @abstractmethod
    def generate(self, diff):
        pass

class BasicChangeDescriptionStrategy(ChangeDescriptionStrategy):
    """
    The `BasicChangeDescriptionStrategy` class is a subclass of `ChangeDescriptionStrategy`. It provides a method `generate` which takes a `diff` object as input and generates a description
    * of the changes in the diff.

    Attributes:
        None

    Methods:
        - `generate(diff)`: Generates a description of the changes in the given `diff` object.

    Example usage:
        basic_strategy = BasicChangeDescriptionStrategy()
        diff = ... (initialize the diff object)
        description = basic_strategy.generate(diff)

    Example output:
        File Added: path/to/file1.py
        File Modified: path/to/file2.py
        File Deleted: path/to/file3.py
        File Renamed (Possible): path/to/file4.py

    """
    def generate(self, diff):
        description = ""
        for change in diff:
            if change.a_path:
                description += f"File Added: {change.a_path}\n"
            elif change.d_path:
                description += f"File Deleted: {change.d_path}\n"
            elif change.b_path:
                description += f"File Modified: {change.b_path}\n"
            else:
                description += f"File Renamed (Possible): {change.a_path or change.b_path}\n"
        return description

class VerboseChangeDescriptionStrategy(ChangeDescriptionStrategy):
    """
    A change description strategy that generates a verbose description of file changes.

    This strategy generates a string description of the file changes in a diff.
    The description includes information about added, deleted, modified, and renamed files,
    as well as the diff details for modified files.

    Attributes:
        None

    Methods:
        generate(diff): Generates the verbose change description for the given diff.
        _generate_diff_summary(change): Generates the diff summary for a modified file.

    Note:
        This class inherits from the ChangeDescriptionStrategy base class.

    Example Usage:
        strategy = VerboseChangeDescriptionStrategy()
        diff = calculate_diff()
        description = strategy.generate(diff)
    """
    def generate(self, diff):
        description = ""
        for change in diff:
            if change.a_path:
                description += f"File Added: {change.a_path}\n"
            elif change.d_path:
                description += f"File Deleted: {change.d_path}\n"
            elif change.b_path:
                description += f"File Modified: {change.b_path}\n"
                description += self._generate_diff_summary(change)  # Add diff details
            else:
                description += f"File Renamed (Possible): {change.a_path or change.b_path}\n"
        return description

    def _generate_diff_summary(self, change):
        summary = "Diff:\n"
        for d in change.diff.iter_change_type('M'):
            summary += f"+ {d.a_blob.data_stream.read().decode()} \n"  # Added lines
            summary += f"- {d.b_blob.data_stream.read().decode()} \n"  # Removed lines
        return summary
