# 导入PyMuPDFLoader类，用于加载PDF文件
from langchain_community.document_loaders import PyMuPDFLoader
# 导入RecursiveCharacterTextSplitter类，用于将文本分割成指定大小的块
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 导入HuggingFaceEmbeddings类，用于将文本转换为向量
from langchain_huggingface import HuggingFaceEmbeddings
# 导入Chroma类，用于将向量存储到数据库中
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

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