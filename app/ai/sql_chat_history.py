from typing import List

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import BaseMessage


class CustomSQLChatMessageHistory(SQLChatMessageHistory):

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

    def get_messages_by_session_id(self, target_session_id: str) -> List[BaseMessage]:
        """
        Retrieve messages for a specific session ID
        """
        with self.Session() as session:
            result = (
                session.query(self.sql_model_class)
                .filter(
                    getattr(self.sql_model_class, self.session_id_field_name)
                    == target_session_id
                )
                .order_by(self.sql_model_class.id.asc())
            )
            messages = []
            for record in result:
                messages.append(self.converter.from_sql_model(record))
            return messages

    def create_conversation(self, session_id: str):
        """
        Create Message object with generated session_id
        """

        empty_message = BaseMessage(content="", type="")
        with self.Session() as session:
            empty_sql_model = self.converter.to_sql_model(empty_message, session_id)
            session.add(empty_sql_model)
            session.commit()

