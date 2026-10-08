import os
import json
import argparse
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DB_DIR = "./chroma_db"

print("Loading local embedding model (all-MiniLM-L6-v2)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def match_job(job_description_path, required_skills=None, min_experience=0):
    if not os.path.exists(job_description_path):
        print(f"Error: Job description file {job_description_path} not found.")
        return
        
    with open(job_description_path, 'r', encoding='utf-8') as f:
        job_description = f.read()
        
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    k_retrieve = 20
    results = vectorstore.similarity_search_with_score(job_description, k=k_retrieve)
    
    if not results:
        print("No results found in the vector database.")
        return
        
    candidates = {}
    
    for doc, distance in results:
        meta = doc.metadata
        source = meta.get('source', 'Unknown')
        name = meta.get('name', 'Unknown')
        
        skills_str = meta.get('skills_str', '')
        skills = [s.strip() for s in skills_str.split(',')] if skills_str else []
        exp = meta.get('years_of_experience', 0)
        
        if exp < min_experience:
            continue
            
        if required_skills:
            skills_lower = [s.lower() for s in skills]
            has_skills = all(req.lower() in skills_lower for req in required_skills)
            if not has_skills:
                continue
                
        if source not in candidates:
            candidates[source] = {
                "candidate_name": name,
                "resume_path": source,
                "all_skills": skills,
                "chunks": [],
                "best_distance": distance
            }
        
        candidates[source]["chunks"].append(doc.page_content)
        if distance < candidates[source]["best_distance"]:
            candidates[source]["best_distance"] = distance

    k_matches = 10
    sorted_candidates = sorted(candidates.values(), key=lambda x: x["best_distance"])[:k_matches]
    
    top_matches = []
    
    for cand in sorted_candidates:
        # Distance heuristic for HuggingFace embeddings
        raw_score = max(0, min(100, int((1.5 - cand["best_distance"]) * 80))) 
        
        # Local fallback reasoning
        matched_skills = [s for s in cand["all_skills"] if s.lower() in job_description.lower()]
        reasoning = f"Matched {len(matched_skills)} relevant skills based on local semantic search."
            
        top_matches.append({
            "candidate_name": cand["candidate_name"],
            "resume_path": cand["resume_path"],
            "match_score": raw_score,
            "matched_skills": matched_skills,
            "relevant_excerpts": cand["chunks"][:2],
            "reasoning": reasoning
        })

    output = {
        "job_description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
        "top_matches": top_matches
    }
    
    print(json.dumps(output, indent=2))
    
    with open('match_results.json', 'w') as f:
        json.dump(output, f, indent=2)
        
    print("\nResults saved to match_results.json")
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match a Job Description against stored resumes.")
    parser.add_argument("jd_path", help="Path to the Job Description text file.")
    parser.add_argument("--req-skills", nargs='+', help="List of required skills.")
    parser.add_argument("--min-exp", type=int, default=0, help="Minimum years of experience required.")
    
    args = parser.parse_args()
    match_job(args.jd_path, args.req_skills, args.min_exp)
