from typing import List, Optional

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.chat_message_histories.sql import BaseMessageConverter
from langchain_core.messages import BaseMessage
from config.settings import settings


class CustomSQLChatMessageHistory(SQLChatMessageHistory):
    """
    This class override SQLChatMessageHistory class from Langchain library
    """

    def __init__(
            self,
            session_id: str,
            table_name: str = "message_store",
            session_id_field_name: str = "session_id",
            custom_message_converter: Optional[BaseMessageConverter] = None,
    ):
        # Hard code the connection_string
        connection_string = settings.SQLITE_CONNECTION_STRING

        super().__init__(
            session_id=session_id,
            connection_string=connection_string,
            table_name=table_name,
            session_id_field_name=session_id_field_name,
            custom_message_converter=custom_message_converter,
        )

    def unique_session_ids(self) -> List[str]:
        """
        Retrieve all unique session IDs from db
        """
        with self.Session() as session:
            result = (
                session.query(getattr(self.sql_model_class, self.session_id_field_name))
                .distinct()
                .all()
            )
            return [row[0] for row in result]

    def get_messages_by_session_id(self) -> List[BaseMessage]:
        """
        Retrieve messages for a specific session ID
        """
        with self.Session() as session:
            result = (
                session.query(self.sql_model_class)
                .filter(
                    getattr(self.sql_model_class, self.session_id_field_name)
                    == self.session_id
                )
                .order_by(self.sql_model_class.id.asc())
            )
            messages = []
            for record in result:
                messages.append(self.converter.from_sql_model(record))
            return messages

    def create_conversation(self):
        """
        Create Message object with generated session_id
        """

        # Because message field is required the content is an empty string and type is system
        # Later in conversation user input is a 'human' type and AI response is 'ai' type
        empty_message = BaseMessage(content="", type="system")
        with self.Session() as session:
            empty_sql_model = self.converter.to_sql_model(empty_message, self.session_id)
            session.add(empty_sql_model)
            session.commit()

    def delete_conversation(self):
        """
        Delete all Message objects with specified session_id
        """

        with self.Session() as session:
            session.query(self.sql_model_class).filter(
                getattr(self.sql_model_class, self.session_id_field_name)
                == self.session_id
            ).delete()
            session.commit()
