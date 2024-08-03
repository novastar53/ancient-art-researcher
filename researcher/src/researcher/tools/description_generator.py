import os
from typing import List, Optional, Dict, Any

from firecrawl import FirecrawlApp 

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from groq import Groq
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


from crewai_tools import BaseTool

from researcher.utils.types import ImageInfo

_firecrawl = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False
        )

_embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

#_chat_model = ChatGroq(temperature=0,
#                    model_name="mixtral-8x7b-32768",
#                    api_key=os.environ.get("GROQ_API_KEY"),)

_chat_model = ChatOpenAI(model="gpt-4o")


class DescriptionGenerator(BaseTool):
    name: str = "Image Description Generator"
    description: str = (
        "Accepts an ImageInfo class object and length. Returns a description of the image of the desired length"
    )


    _rag_template = """\
    Use the context to gen erate a {length} word description of an image based on content
    taken from the image's source website.

    Image Details:
    - Title: {title}
    - Url: {image_url}
    - Source Website Url: {source_url}

    Source Website Content:
    {content}
    """
    _rag_prompt = ChatPromptTemplate.from_template(_rag_template)


    def _scrape(self, url: str):

        try:
            options = {
                "extractorOptions": {},
                "pageOptions": {
                    'onlyMainContent': True,
                },
                "timeout": 40000,
            }
            return _firecrawl.scrape_url(url, options)["content"]
        except:
            return ""


    def _run(self, image_info: ImageInfo, output_num_words: int) -> str:
        """
        Generates descriptions from metadata and source website content.

        Parameters:
        Image_info (ImageInfo): Metadata about the image
        output_num_words: The number of words to generate

        Returns:
        str: The generated output

        """

        # Scrape all the content from the image source website
        scraped_content = self._scrape(image_info.link)        

        # Naively chunk the document into sections of similar length
        naive_chunks = _text_splitter.split_text(scraped_content)

        # Embed the chunks using an embedding model
        naive_chunk_vectorstore = Chroma.from_texts(naive_chunks, embedding=_embed_model)
        naive_chunk_retriever = naive_chunk_vectorstore.as_retriever(search_kwargs={"k" : 5},)


        # Find the most relevant chunk using a similarity metric 
        relevant_chunks = naive_chunk_retriever.get_relevant_documents(f"image title: {image_info.title}, image source: {image_info.source}")

        # Find the chunk with the image URL inside it

        # Concat the two chunks
        relevant_content = "\n".join([r.page_content  for r in relevant_chunks])

        # Generate a prompt for the (expensive) content generation model

        prompt_args = {
            "length": str(output_num_words),
            "title": image_info.title,
            "image_url": image_info.source,
            "source_url": image_info.link,
            "content": relevant_content         
        }

        def _get_prompt():
            return self._rag_template.format(**prompt_args)

        rag_chain = (
             _chat_model
            | StrOutputParser()
        )

        # Retrieve the model output and return it
        generated_text =  rag_chain.invoke(_get_prompt())
        return generated_text
        
