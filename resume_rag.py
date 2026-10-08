import os
import glob
import json
import re
from PyPDF2 import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DB_DIR = "./chroma_db"
RESUME_DIR = "./resumes"
os.makedirs(RESUME_DIR, exist_ok=True)

print("Loading local embedding model (all-MiniLM-L6-v2)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text


def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
    return text


def extract_metadata_heuristic(text, file_path):
    """
    Extracts basic metadata using regex and simple string matching.
    This replaces the LLM to run entirely locally and for free.
    """
    # Use the filename as a fallback for the name
    filename = os.path.basename(file_path)
    meta = {"name": filename, "skills": [], "years_of_experience": 0, "education": []}
    
    # Very basic heuristic for years of experience (looks for "X years")
    exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?).*?(?:experience|exp)', text, re.IGNORECASE)
    if exp_match:
        try:
            meta["years_of_experience"] = int(exp_match.group(1))
        except:
            pass
            
    # Simple predefined skills list for heuristic matching
    common_skills = ["Python", "Java", "C++", "C#", "Machine Learning", "Data Science", "SQL", "React", "Angular", "Node.js", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Linux", "Git", "TensorFlow", "PyTorch", "NLP", "Computer Vision"]
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    meta["skills"] = found_skills
    
    return meta


def process_resumes():
    files = glob.glob(os.path.join(RESUME_DIR, "**", "*.[pd][do][fc]*"), recursive=True)
    
    if not files:
        print(f"No resumes found in {RESUME_DIR}. Please add some PDFs or DOCX files.")
        return
        
    documents = []
    
    for file_path in files:
        print(f"Processing {file_path}...")
        if file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx') or file_path.lower().endswith('.doc'):
            text = extract_text_from_docx(file_path)
        else:
            continue
            
        if not text.strip():
            print(f"Could not extract text from {file_path}")
            continue
            
        # Extract Metadata (using heuristics instead of OpenAI)
        metadata = extract_metadata_heuristic(text, file_path)
        metadata['source'] = file_path
        
        # Convert lists to comma-separated strings as ChromaDB metadata only supports str, int, float, bool
        metadata['skills_str'] = ", ".join(metadata.get('skills', []))
        metadata['education_str'] = ", ".join(metadata.get('education', []))
        
        if 'skills' in metadata: del metadata['skills']
        if 'education' in metadata: del metadata['education']
        
        # Intelligent Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        
        for i, chunk in enumerate(chunks):
            chunk_meta = metadata.copy()
            chunk_meta['chunk_id'] = i
            documents.append({
                "page_content": chunk,
                "metadata": chunk_meta
            })
            
    if not documents:
        print("No documents were parsed into chunks.")
        return
        
    print(f"Extracted {len(documents)} chunks from {len(files)} resumes.")
    
    print("Ingesting into vector database...")
    vectorstore = Chroma.from_texts(
        texts=[doc["page_content"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print("Successfully ingested documents and persisted ChromaDB.")

if __name__ == "__main__":
    process_resumes()
