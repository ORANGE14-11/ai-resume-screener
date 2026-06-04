from sentence_transformers import SentenceTransformer, util

class ResumeMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def compute_similarity(self, resume_text, job_text):
        resume_sentences = [s.strip() for s in resume_text.split('.') if len(s) > 20]
        job_sentences = [s.strip() for s in job_text.split('.') if len(s) > 20]
        
        if not resume_sentences or not job_sentences:
            return {'score': 0, 'missing_keywords': ['Not enough text to analyze'], 'suggestions': ['Add more content to your resume/job description']}
        
        resume_embeddings = self.model.encode(resume_sentences, convert_to_tensor=True)
        job_embeddings = self.model.encode(job_sentences, convert_to_tensor=True)
        
        similarity_matrix = util.cos_sim(resume_embeddings, job_embeddings)
        best_matches = similarity_matrix.max(dim=0)[0]
        overall_score = float(best_matches.mean().item() * 100)
        
        missing_threshold = 0.4
        missing_indices = [i for i, score in enumerate(best_matches) if score < missing_threshold]
        missing_keywords = [job_sentences[i][:80] for i in missing_indices[:5]]
        
        return {
            'score': round(overall_score, 1),
            'missing_keywords': missing_keywords if missing_keywords else ['None! Great match!'],
            'suggestions': [f'Add: {kw}' for kw in missing_keywords[:3]] if missing_keywords else ['Your resume looks excellent!']
        }
