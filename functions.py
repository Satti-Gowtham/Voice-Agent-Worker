import logging, pyperclip, asyncio, os
from typing import Annotated, List, Tuple
from livekit.agents import llm
from datetime import datetime
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

DB_PATH = "./DB"

class AssistantFunctions(llm.FunctionContext):
    logger = logging.getLogger("Function-call")
                
    @llm.ai_callable()
    async def get_data_time(self):
        self.logger.info(f"getting date and time details")
        now = datetime.now()
        return f"The current date is {now:%b-%d-%Y}. The current time is {now:%H:%M:%S}"
    
    @llm.ai_callable()
    async def get_context_from_db(
        self,
        query: Annotated [
            str,
            llm.TypeInfo(description="The query used to retrieve information from the database when users ask about specific topics.")
        ]
    ):
        self.logger.info(f"getting context for query")
        
        return await self.get_context(query)

    @llm.ai_callable()
    def get_clipboard_text(
        self
    ):
        try:
            clipboard_text = pyperclip.paste()  # Get text from clipboard
            self.logger.info("Retrieved text from clipboard successfully.")

            return clipboard_text
        except Exception as e:
            self.logger.error(f"Failed to retrieve text from clipboard: {e}")

            raise RuntimeError("Unable to access clipboard text.") from e
    
    def get_embedding_function(self):
        return OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=os.getenv("OLLAMA_BASE_URL")
        )

    async def get_context(self, query: str):
        # Prepare the DB.
        embedding_function = self.get_embedding_function()
        db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_score(query, k=3)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

        return context_text