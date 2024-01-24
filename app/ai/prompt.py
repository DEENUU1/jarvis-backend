from langchain.prompts import PromptTemplate
from schemas.user import User

template = PromptTemplate.from_template(
    "You are Jarvis an AI assistant which helps me in every day tasks. "
    "You always need to tell the truth, if you don't know the answer you can use tools. " 
    "You follow the instructions you receive from the user as best as you can. "
    "Feel free to use any tools available to look up. "
    "User data: {user} "
)

user = User()
prompt = template.format(
    user=f"first name: {user.first_name} last name: {user.last_name} location: {user.location}"
)

