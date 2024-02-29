import openai
from models import CommitOutput  # Assuming models.py contains all Pydantic models
from config import ConfigManager

CONFIG_MANAGER = ConfigManager()
OPENAI_API_KEY = CONFIG_MANAGER.app_config.get_config_value('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def generate_commit_output(commit) -> CommitOutput:
    if commit.parents:
        diff = commit.parents[0].diff(commit)
        change_description = ""  # generate_change_description(diff)
    else:
        change_description = ""
    output = CommitOutput(
        commit_hash=commit.hexsha,
        author=commit.author.name,
        date=commit.authored_datetime,
        message=commit.message.strip(),
        change_description=change_description,
    )
    return output


def generate_change_description(diff) -> str:
    diff_summary = ""
    for d in diff:
        diff_summary += f'{d.change_type} {d.a_path}\n'
    response = openai.Completion.create(
        engine="text-davinci-003",  # Using the davinci model which is best-suited for writing style tasks.
        prompt=diff_summary,
        temperature=0.5,  # You could experiment with this value according to the level of randomness you desire.
        max_tokens=100  # This limits the length of the output. Adjust it according to your needs.
    )
    return response.choices[0].text.strip()


def sanitize_for_html(text: str) -> str:
    return text.replace("\n", "<br>")
