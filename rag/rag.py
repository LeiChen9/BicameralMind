# 导入PyMuPDFLoader类，用于加载PDF文件
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import JSONLoader
# 导入RecursiveCharacterTextSplitter类，用于将文本分割成指定大小的块
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 导入HuggingFaceEmbeddings类，用于将文本转换为向量
from langchain_huggingface import HuggingFaceEmbeddings
# 导入Chroma类，用于将向量存储到数据库中
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
import getpass
import os
import pdb
os.environ["TOKENIZERS_PARALLELISM"] = "false"

MAX_BATCH_SIZE = 41666

def pdf_rag_build(input_file):
    if input_file.endswith('.pdf'):
        # 创建PyMuPDFLoader对象，加载PDF文件
        loader = PyMuPDFLoader("../data/Symbolic.pdf")
        # 加载PDF文件中的数据
        PDF_data = loader.load()

    # 创建RecursiveCharacterTextSplitter对象，将文本分割成指定大小的块
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=5)
    # 将PDF数据分割成块
    all_splits = text_splitter.split_documents(PDF_data)

    # 定义模型名称和参数
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    # 创建HuggingFaceEmbeddings对象，将文本转换为向量
    embedding = HuggingFaceEmbeddings(model_name=model_name,
                                    model_kwargs=model_kwargs)

    # 定义持久化目录
    persist_directory = 'db'
    # 创建Chroma对象，将向量存储到数据库中
    vectordb = Chroma.from_documents(documents=all_splits, embedding=embedding, persist_directory=persist_directory)
    
    return vectordb 

def metadata_func(record: dict, metadata: dict) -> dict:
    # metadata["id"] = record["id"]
    metadata["question"] = record["QUESTION"]
    metadata["labels"] = ",".join(record["LABELS"])
    metadata["long_answer"] = record["LONG_ANSWER"]
    metadata["meshes"] = ",".join(record["MESHES"])
    metadata["final_decision"] = record.get("final_decision", "Unknown")
    # 由于"CONTEXTS"是我们要向量化的文本，我们将其作为列表传递
    metadata["page_content"] = " ".join(record["CONTEXTS"])
    return metadata

def split_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

if __name__ == '__main__':
    # db = rag_build('Symbolic.pdf')
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 注意这里的文件路径需要替换为您实际的文件路径
    loader = JSONLoader(
        file_path="../datasets/pubmedqa/data/pqaa_train_set.json",
        jq_schema='.[]',
        content_key="CONTEXTS",
        metadata_func=metadata_func,
        text_content=False,
    )
    documents = loader.load()
    
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=5)
    # 将PDF数据分割成块
    split_docs = text_splitter.split_documents(documents)
    
    split_docs_chunked = split_list(split_docs, 41000)
    
    for split_docs_chunk in split_docs_chunked:
        vectorstore = Chroma.from_documents(
            documents=split_docs_chunk,
            embedding=embedding_function,
            persist_directory='./db',
        )
        vectorstore.persist()
    
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=5)
    # documents =  text_splitter.split_documents(documents=documents)
    
    # vectorstore = Chroma.from_documents(documents, embedding_function)
    
    retriever = vectorstore.as_retriever()
    
    os.environ["OPENAI_API_KEY"] = getpass.getpass()
    openai_key = os.environ["OPENAI_API_KEY"]
    llm = ChatOpenAI(openai_api_key=openai_key, openai_api_base='http://127.0.0.1:8080/v1')
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever,
        verbose=True
    )
    
    query = "Tell me about Gly-P1"
    qa.invoke(query)
    print(qa.get_answers(query))