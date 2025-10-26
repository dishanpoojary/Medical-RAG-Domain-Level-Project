# Medical RAG Chatbot System (NVIDIA API & Pinecone)

This project implements a Retrieval-Augmented Generation (RAG) system for medical question-answering. It uses LangChain to connect a vector database (Pinecone) containing domain-specific documents with a powerful Large Language Model (LLM) hosted on the NVIDIA AI Endpoints.

## ⚙️ Tech Stack & Architecture

* **Framework:** Python, Flask
* **Vector Database:** Pinecone (Serverless)
* **LLM Provider:** NVIDIA AI Endpoints (via the `ChatOpenAI` wrapper or `ChatNVIDIA` class)
* **Embeddings:** HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
* **Orchestration:** LangChain v0.x / v1.x (mixed environment for stability)

***

## 🚀 Local Setup and Run Instructions

This guide assumes you have **Anaconda/Conda** installed for environment management.

### STEP 01: Environment Setup

Since our stable setup relied on a specific version mix, we must use the dedicated environment name.

1.  **Activate Environment:** Open your terminal and activate the environment where you ran the code:
    ```bash
    conda activate medibot_nvidia
    ```

### STEP 02: Install Dependencies

Since you successfully ran the project, your dependencies should be installed. If starting on a new machine, run:
```bash
pip install -r requirements.txt


STEP 03: Configure API Keys
Create a file named .env in the root directory and add your credentials.

Note: The LLM uses the NVIDIA API, but the LangChain integration requires the key to be loaded as NVIDIA_API_KEY.

# .env file

# Get this key from the NVIDIA AI Catalog / NGC
NVIDIA_API_KEY="nvapi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Get this key from app.pinecone.io
PINECONE_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

Since you successfully completed the entire project setup, implemented the RAG chain using the NVIDIA endpoint, and fixed all the environment issues, your README file should document the final, working architecture, and include the correct instructions (which now rely on the modern and stable practices we established).

Here is the recommended text content for your README.md. It uses the NVIDIA LLM and the compatible LangChain v1.x architecture.

Markdown

# Medical RAG Chatbot System (NVIDIA API & Pinecone)

This project implements a Retrieval-Augmented Generation (RAG) system for medical question-answering. It uses LangChain to connect a vector database (Pinecone) containing domain-specific documents with a powerful Large Language Model (LLM) hosted on the NVIDIA AI Endpoints.

## ⚙️ Tech Stack & Architecture

* **Framework:** Python, Flask
* **Vector Database:** Pinecone (Serverless)
* **LLM Provider:** NVIDIA AI Endpoints (via the `ChatOpenAI` wrapper or `ChatNVIDIA` class)
* **Embeddings:** HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
* **Orchestration:** LangChain v0.x / v1.x (mixed environment for stability)

***

## 🚀 Local Setup and Run Instructions

This guide assumes you have **Anaconda/Conda** installed for environment management.

### STEP 01: Environment Setup

Since our stable setup relied on a specific version mix, we must use the dedicated environment name.

1.  **Activate Environment:** Open your terminal and activate the environment where you ran the code:
    ```bash
    conda activate medibot_nvidia
    ```

### STEP 02: Install Dependencies

Since you successfully ran the project, your dependencies should be installed. If starting on a new machine, run:
```bash
pip install -r requirements.txt

## STEP 03: Configure API Keys
Create a file named .env in the root directory and add your credentials.

Note: The LLM uses the NVIDIA API, but the LangChain integration requires the key to be loaded as NVIDIA_API_KEY.


# .env file

# Get this key from the NVIDIA AI Catalog / NGC
NVIDIA_API_KEY="nvapi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Get this key from app.pinecone.io
PINECONE_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

###STEP 04: Process Data and Store Index
Run the script to load PDFs from the ./data folder, generate embeddings, and upload them to your Pinecone index (medical-chatbot).
python store_index.py

(Ensure your PDFs are inside the ./data directory before running.)

###STEP 05: Run the Flask Application
Start the web server:
python app.py
The application will start running on the local development server.

###STEP 06: Access the Chatbot
Open your web browser and navigate to the local address displayed in the terminal (usually port 5000 or 8080):

http://localhost:5000
(If you changed the port in app.py, use that port number instead.)


☁️ AWS CICD Deployment (Outline)
The following steps outline the general process for deploying this system using GitHub Actions and AWS services, which is the next stage of your project.

Login to AWS Console.

Create IAM User for Deployment: Grant access for EC2 (Virtual Machine) and ECR (Elastic Container Registry).

Policies: AmazonEC2ContainerRegistryFullAccess, AmazonEC2FullAccess.

Create ECR Repo: Create a repository to store your Docker image.

Example URI: 315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot

Create EC2 Machine (Ubuntu): This will be the host for the application.

Install Docker in EC2: Install Docker and configure the ubuntu user to run Docker commands.

Configure EC2 as Self-Hosted Runner (for CI/CD): Set up the EC2 instance to run GitHub Actions jobs (Build, Push, Deploy).

Setup GitHub Secrets: Add necessary secrets to your GitHub repository for the CI/CD pipeline.

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_DEFAULT_REGION

ECR_REPO

PINECONE_API_KEY

NVIDIA_API_KEY