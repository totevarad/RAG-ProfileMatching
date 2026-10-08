# Implementation Plan & Evaluations

This document outlines the step-by-step implementation plan for the RAG-Based Profile Matching system, along with evaluation criteria for each phase to ensure the system meets the assignment requirements.

## Phase 1: Environment Setup & Data Collection

### Implementation
1. **Repository Setup:** Initialize the project structure and create required files (`resume_rag.py`, `job_matcher.py`, Jupyter Notebook).
2. **Dependency Management:** Set up a virtual environment and install necessary libraries (e.g., `langchain`, `chromadb`/`pinecone`, `openai`/`sentence-transformers`, `PyPDF2`).
3. **Data Collection:** Gather a diverse dataset of 30+ resumes (PDF/DOCX) and 5+ detailed job descriptions, representing various roles and experience levels.

### Evaluation
- **Data Completeness:** Verify the dataset contains exactly or more than the required number of resumes and JDs.
- **Data Diversity:** Ensure resumes cover different fields, formats, and skill sets to test the system's robustness.
- **Environment:** Successfully load a sample resume and job description using basic Python I/O without dependency errors.

---

## Phase 2: Document Processing Pipeline (`resume_rag.py`)

### Implementation
1. **Document Loading:** Implement functions to parse text from raw PDF and DOCX resume files.
2. **Metadata Extraction:** Use regex, NLP tools (like spaCy), or LLM prompts to extract Name, Skills, Years of Experience, and Education from the raw text.
3. **Intelligent Chunking:** Implement a chunking strategy that splits the document while preserving semantic boundaries (e.g., keeping the "Education" section in one chunk if possible, or using overlap).

### Evaluation
- **Extraction Accuracy:** Randomly sample 5 resumes and manually verify that the extracted Name, Skills, Experience, and Education exactly match the document contents.
- **Chunk Quality:** Inspect the generated chunks for a few resumes to ensure sections aren't cut off awkwardly mid-sentence or mid-concept.

---

## Phase 3: Embedding & Vector Database Integration (`resume_rag.py`)

### Implementation
1. **Embedding Generation:** Select an embedding model (e.g., `text-embedding-3-small` or HuggingFace equivalent) and convert the text chunks into vectors.
2. **Vector DB Setup:** Initialize a local or cloud vector database (e.g., ChromaDB).
3. **Data Ingestion:** Upsert the embeddings along with their corresponding metadata (extracted in Phase 2) into the vector database.

### Evaluation
- **Ingestion Success:** Query the database for the total number of vectors and verify it matches the expected number of chunks generated.
- **Metadata Retrieval:** Perform a dummy query to ensure that when a vector is retrieved, its attached metadata (Name, Skills, etc.) is correctly returned alongside it.
- **Latency (Ingestion):** Measure and record the time taken to embed and store all 30+ resumes.

---

## Phase 4: Semantic Search & Job Matching Engine (`job_matcher.py`)

### Implementation
1. **JD Processing:** Implement the pipeline to take a raw job description, optionally extract key requirements, and generate its vector embedding.
2. **Semantic Retrieval:** Query the vector database with the JD embedding to retrieve the top 10 most relevant resume chunks.
3. **Hybrid Search Integration:** Enhance the search by combining vector similarity with a keyword filter (e.g., BM25 or strict metadata filtering for must-have skills).
4. **Scoring Mechanism:** Develop an algorithm to calculate a 0-100 match score based on vector distance, keyword matches, and metadata alignment.

### Evaluation
- **Retrieval Accuracy:** For the 5 test JDs, manually review the Top-K (K=10) retrieved resumes. Ensure the retrieved profiles are logically a good fit for the JD.
- **Filter Efficacy:** Test a JD with a strict requirement (e.g., "Must have Python"). Verify that resumes lacking "Python" in their skills metadata are appropriately down-ranked or filtered out.
- **Scoring Logic:** Ensure the 0-100 score correlates with the actual quality of the match (e.g., a perfect match gets >90, partial matches get 50-80).

---

## Phase 5: Output Formatting & Reasoning Generation

### Implementation
1. **Match Reasoning:** Use an LLM (or a deterministic rule-based string generator) to provide a 1-2 sentence reasoning explaining *why* the candidate matched, referencing specific skills or chunks.
2. **JSON Construction:** Format the final output exactly as specified in the assignment requirements.

### Evaluation
- **Schema Validation:** Validate the output of the matching engine against the required JSON schema.
- **Reasoning Quality:** Review the generated reasoning strings for clarity and accuracy based on the provided `relevant_excerpts` and `matched_skills`.

---

## Phase 6: Experimentation & Documentation

### Implementation
1. **Jupyter Notebook Analysis:** Document the process, compare different chunking sizes, or compare two different embedding models in the notebook.
2. **Performance Metrics Compilation:** Finalize the latency and accuracy metrics.
3. **Demo Video Recording:** Record the 3-4 minute video demonstrating the end-to-end pipeline.

### Evaluation
- **Notebook Completeness:** Ensure the notebook tells a clear story of the experimentation process with visible outputs.
- **System Latency:** Measure the end-to-end time for a single JD query to return the JSON result. It should ideally be under a few seconds.
- **Demo Clarity:** Verify the demo video clearly shows the input JD, the terminal execution, and the final JSON output.
