# RAG-Based Profile Matching: Problem Statement

## Brief
This assignment focuses on building a Retrieval-Augmented Generation (RAG) based Profile Matching system. You will develop a system capable of ingesting resumes, processing them into vector representations, and matching them against specific job descriptions using semantic search techniques.

## Learning Objectives
By completing this assignment, you will learn to:
- **Implement document chunking and embedding:** Effectively process unstructured document data (resumes) into manageable chunks.
- **Build vector databases:** Set up and manage a vector database to store and efficiently query embeddings.
- **Create retrieval pipelines:** Design end-to-end pipelines that connect document ingestion, embedding generation, and database storage.
- **Understand semantic search:** Apply semantic search capabilities to retrieve relevant documents based on context and meaning rather than just keyword matching.

## Assignment Requirements

### Part A: RAG System Setup (50%)
**Target File:** `resume_rag.py`

#### 1. Document Processing Pipeline
- **Load Resumes:** Utilize file system tools (from Milestone 1) to load resume files (e.g., PDFs, DOCX).
- **Intelligent Chunking:** Parse and chunk documents intelligently, ensuring that critical sections like "Education", "Experience", and "Skills" are preserved and not split awkwardly.
- **Generate Embeddings:** Use embeddings models such as OpenAI, Cohere, or HuggingFace to convert text chunks into vector representations.
- **Vector Database Storage:** Store the generated embeddings in a robust vector database (choose between ChromaDB, Pinecone, or Weaviate).

#### 2. Metadata Extraction
- **Extract Key Fields:** Parse the resumes to extract structured metadata, specifically:
  - Name
  - Skills
  - Years of Experience
  - Education
- **Store Metadata:** Save this extracted metadata alongside the vector embeddings in your database to enable precise filtering during retrieval.

### Part B: Job Matching Engine (50%)
**Target File:** `job_matcher.py`

#### 1. Semantic Search
- **Job Description Input:** The system must accept a raw job description (JD) as input.
- **Embedding Generation:** Convert the provided JD into its vector embedding representation.
- **Retrieval:** Query the vector database to retrieve the top-K (where K=10) most similar resumes based on semantic meaning.
- **Hybrid Search:** Implement a hybrid search approach combining semantic similarity with keyword matching (especially for critical, non-negotiable skills).

#### 2. Ranking & Scoring
- **Score Matches:** Calculate a match score for each retrieved resume on a scale of 0-100.
- **Provide Reasoning:** The system must output the reasoning behind the match score (e.g., specifying which sections or skills matched the JD).
- **Requirements Filtering:** Apply filters for must-have requirements based on metadata (e.g., filtering out candidates without "5+ years Python" if specified).

### Output Format
The engine should produce results in the following JSON structure:

```json
{
  "job_description": "...",
  "top_matches": [
    {
      "candidate_name": "John Doe",
      "resume_path": "resumes/john_doe.pdf",
      "match_score": 92,
      "matched_skills": [
        "Python",
        "Machine Learning"
      ],
      "relevant_excerpts": [
        "..."
      ],
      "reasoning": "Strong match for ML experience..."
    }
  ]
}
```

## Submission Guidelines

### Deliverables
Please ensure the following deliverables are included in your submission:
1. **Complete RAG Implementation:** The fully functional Python scripts (`resume_rag.py` and `job_matcher.py`) and any supporting code.
2. **Dataset:** A curated dataset containing:
   - 30+ diverse resumes
   - 5+ job descriptions
3. **Jupyter Notebook:** A notebook detailing your experimentation, analysis, and thought process during the development.
4. **Performance Metrics:** Documentation of your system's performance, including:
   - Retrieval accuracy
   - System latency
5. **Demo Video:** A 3-4 minute recorded demonstration showcasing the working system.
