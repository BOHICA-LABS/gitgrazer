from openai import OpenAI
from models import CommitOutput, ChangeDescription
from config import ConfigManager

CONFIG_MANAGER = ConfigManager()
OPENAI_API_KEY = CONFIG_MANAGER.app_config.get_config_value('OPENAI_API_KEY')
CLIENT = OpenAI(api_key=OPENAI_API_KEY)

TEMPLATE = (
    "Based on the git diff output provided: /n"
    "{{diff}}/n"
    "Analyze the code changes meticulously. Your task is to dissect the adjustments, identifying what has been added, "
    "removed, or altered. Delve into the purpose behind these changes, reflecting on how they align with or diverge " 
    "from the project's goals. Examine the impact these modifications may have on the project's functionality, "
    "considering both immediate effects and potential long-term consequences. "
    "Moreover, evaluate the adherence to or deviation from coding standards and best practices. Consider why certain " 
    "patterns might have been introduced or eliminated, and what this suggests about the project's evolving "
    "requirements or objectives. Provide a reasoned analysis that connects the changes to broader development "
    "practices and principles. "
    "Your analysis should be comprehensive and insightful, offering a deep understanding of the commit's intentions " 
    "and effects. Approach this with confidence, assuming familiarity with the relevant coding paradigms and the "
    "project's overarching aims. Present your findings in a clear, narrative form, weaving in any recommendations for "
    "further enhancements or adjustments. Your evaluation should be as conclusive as possible, reflecting a high "
    "degree of certainty in your interpretations.")


def generate_commit_output(commit) -> CommitOutput:
    if commit.parents:
        diff = commit.parents[0].diff(commit)
        change_description = generate_change_description(diff)
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


def generate_change_description(diff) -> ChangeDescription:
    diff_summary = ""
    for d in diff:
        diff_summary += f'{d.change_type} {d.a_path}\n'
    # Use the openai.ChatCompletion.create API
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",  # Recommended model for chat-based tasks.
        messages=[
            {"role": "system",
             "content": ("You are a senior developer and code reviewer who specializes in decoding and explaining the "
                         "Git commit history. Your expertise allows you to identify patterns, design decisions, and "
                         "understand what changes occurred in each commit. Your role is to clearly articulate the work "
                         "completed in each commit to provide insight into the project's evolution and development "
                         "strategies. By investigating the Git commits, you create a narrative that depicts how the "
                         "project has evolved over time.")},
            {"role": "user", "content": TEMPLATE.replace("{{diff}}", diff_summary)}
        ]
    )
    # Extract the response
    content = response.choices[0].message.content.strip()

    return ChangeDescription(content=content, diff_summary=diff_summary)


def sanitize_for_html(text: str) -> str:
    return text.replace("\n", "<br>")
