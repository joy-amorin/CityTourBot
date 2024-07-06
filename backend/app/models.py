from sqlmodel import SQLModel, Field

class Conversation(SQLModel, table=True):

    id: int = Field(primary_key=True)
    user_message: str
    bot_response: str