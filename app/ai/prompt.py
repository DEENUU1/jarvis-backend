from langchain.prompts import PromptTemplate
from .tools.today import get_current_time
from schemas.user import User


template = PromptTemplate.from_template(
    "You are an AI assistant called Jarvis, you address the user by his first name. "
    "You follow the instructions you receive from the user as best as you can. "
    ""
    "User data: {user} "
    ""
    "Current time: {datetime} "
    ""
)

current_time = get_current_time()
user = User()
prompt = template.format(
    user=f"first name: {user.first_name} last name: {user.last_name} location: {user.location}",
    datetime=current_time
)
print(prompt)
