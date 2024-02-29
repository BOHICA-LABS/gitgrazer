from abc import ABC, abstractmethod

class ChangeDescriptionStrategy(ABC):
    @abstractmethod
    def generate(self, diff):
        pass

class BasicChangeDescriptionStrategy(ChangeDescriptionStrategy):
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
