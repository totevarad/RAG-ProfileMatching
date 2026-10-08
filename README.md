# RAG-Based Profile Matching System

This project is a Retrieval-Augmented Generation (RAG) system designed to ingest resumes (PDFs and DOCXs), chunk and embed them using offline models, and semantically match them against a Job Description. 

It is designed to run **100% locally and offline** without requiring external API keys or credits.

## Prerequisites & Setup

### 1. Install Dependencies
Make sure you are using a Python virtual environment or installing directly to your global environment. Run:
```bash
pip install -r requirements.txt
```

*(Note: If you run into Application Control / AppLocker blocks on Windows while using a virtual environment, please deactivate your `.venv` and install the requirements globally).*

### 2. Prepare Data Directories

**Resumes Data**
Due to the large number of resumes, they are not pushed to this repository. You must download them manually and place them in the `resumes` directory.
1. Download the Kaggle Resume Dataset from: [https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data)
2. Extract the downloaded archive.
3. Create a `resumes/` folder in the root directory.
4. Place all the extracted candidate resumes inside the `resumes/` folder. The system will recursively search any sub-folders (domains) you create inside it.

*(Note: The `resumes/` folder is included in `.gitignore` to prevent pushing large volumes of data.)*

**Job Descriptions**
Place your Job Description text files inside the `jds/` folder. (e.g. `jds/sample_jd.txt`).

---

## Usage

### Phase 1: Ingestion & Vector Storage
Before you can match a job, you must process your resumes. The `resume_rag.py` script will read all documents, chunk them, extract metadata (skills, years of experience), generate embeddings using `all-MiniLM-L6-v2`, and save everything to a local Chroma database.

Run the ingestion script:
```bash
python resume_rag.py
```
*You only need to run this once, or whenever you add new resumes to the folder.*

### Phase 2: Job Matching & Semantic Search
Once the Chroma database is populated, you can use the `job_matcher.py` script to find the top candidates.

#### **Example 1: Basic Semantic Search**
To run a pure semantic search comparing the JD against all resumes:
```bash
python job_matcher.py jds/sample_jd.txt
```

#### **Example 2: Hybrid Search with Must-Have Skills**
If the job absolutely requires specific skills (e.g., Python and SQL), you can apply hard-filters before the ranking phase using the `--req-skills` flag:
```bash
python job_matcher.py jds/sample_jd.txt --req-skills Python SQL
```
*(Candidates who do not have both Python and SQL extracted in their metadata will be completely ignored, regardless of semantic similarity).*

#### **Example 3: Filtering by Minimum Experience**
To filter out junior candidates who don't meet a minimum threshold (e.g., 3 years):
```bash
python job_matcher.py jds/sample_jd.txt --min-exp 3
```

#### **Example 4: Combining All Filters**
You can combine semantic search with both skill and experience hard-filters for maximum precision:
```bash
python job_matcher.py jds/sample_jd.txt --req-skills "Machine Learning" Python --min-exp 5
```

## Output
The script will print the results to the terminal and simultaneously generate a `match_results.json` file in your workspace containing the Top 10 matches, their match scores (0-100), relevant text excerpts, and matching reasoning.

