from flask import Flask, render_template, jsonify, request
# Ensure helper.py uses correct v1.x imports
from src.helper import download_hugging_face_embeddings
# Correct v1.x imports
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI # Wrapper for NVIDIA endpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import system_prompt # Import specific variable
from pinecone import Pinecone # Import Pinecone client
import os

app = Flask(__name__)

# --- Load Environment Variables ---
print("Loading environment variables...")
load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY')

if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY not found in environment.")
if not NVIDIA_API_KEY:
    raise ValueError("❌ NVIDIA_API_KEY not found in environment.")
print("✅ API keys loaded.")

# --- Initialize Components ---
# Initialize Embeddings FIRST
print("Initializing embeddings...")
embeddings = download_hugging_face_embeddings()
print("✅ Embeddings loaded.")

# Initialize Pinecone Client and Vector Store SECOND
print("Initializing Pinecone...")
index_name = "medical-rag-chatbot" # Your index name
try:
    # Initialize Pinecone Client (v3+)
    pc = Pinecone(api_key=PINECONE_API_KEY)
    # Get the index object
    index = pc.Index(index_name)
    # Initialize LangChain Vector Store with the index object AND embeddings
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
    print("✅ Pinecone vector store connected.")
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize Pinecone: {e}")

# Initialize Retriever THIRD
print("Initializing Retriever...")
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
print("✅ Retriever created.")

# Initialize LLM FOURTH
print("Initializing LLM via NVIDIA endpoint...")
# Configure ChatOpenAI for NVIDIA
nvidia_base_url = "https://integrate.api.nvidia.com/v1"
# Verify model name is correct and available via your NVIDIA API key
nvidia_model_name = "openai/gpt-oss-120b"
try:
    llm = ChatOpenAI(
        model=nvidia_model_name,
        openai_api_key=NVIDIA_API_KEY,
        openai_api_base=nvidia_base_url,
        temperature=0.7 # Adjust as needed
    )
    # Optional: Quick test
    # llm.invoke("test")
    print(f"✅ LLM initialized ({nvidia_model_name}).")
except Exception as e:
     raise RuntimeError(f"❌ Failed to initialize LLM via NVIDIA endpoint: {e}")

# Define Prompt and Chain LAST
print("Defining prompt and chain...")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
print("✅ RAG chain created.")


# --- Flask Routes ---
@app.route("/")
def index():
    # Make sure 'chat.html' exists in a 'templates' folder
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        input_text = msg
        print(f"Received message: {input_text}")
        # Invoke the RAG chain
        response = rag_chain.invoke({"input": input_text})
        answer = response.get("answer", "Sorry, I encountered an issue processing the answer.")
        print(f"Generated response: {answer}")
        return str(answer)
    except Exception as e:
        print(f"❌ Error during chat processing: {e}")
        # Provide a user-friendly error message
        return "Sorry, I couldn't process your request due to an internal error. Please try again later."


if __name__ == '__main__':
    print("Starting Flask app...")
    # Consider setting debug=False for production
    app.run(host="0.0.0.0", port=5000, debug=True)