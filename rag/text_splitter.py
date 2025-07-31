# Recursive character text splitter for Markdown knowledge base
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_markdown(markdown_text: str, chunk_size: int = 500, chunk_overlap: int = 50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n# ", "\n", ". ", " "]
    )
    return splitter.split_text(markdown_text)
