import os
import re
from omegaconf import OmegaConf
from transformers import pipeline


class QuestionAnsweringModel:
    def __init__(self, config_path: str):
        self.config = OmegaConf.load(config_path)

        config_dir = os.path.dirname(os.path.abspath(config_path))
        project_root = os.path.dirname(config_dir)
        data_path = os.path.join(project_root, self.config.data_path)

        with open(data_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        self.sentences = self._split_sentences(raw_text)

        self.qa_pipeline = pipeline(
            "question-answering",
            model=self.config.model_path,
            tokenizer=self.config.model_path,
            device=-1
        )

    # CLEAN TEXT
    def _clean_text(self, text):
        return re.sub(r"[^\w\s]", "", text.lower())

    # SPLIT SENTENCES
    def _split_sentences(self, text):
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    # RETRIEVE CONTEXT
    def _retrieve_context(self, question, top_k=3):
        q_words = set(self._clean_text(question).split())

        scored = []

        for sent in self.sentences:
            s_words = set(self._clean_text(sent).split())

            overlap = len(q_words & s_words)

            if overlap > 0:
                scored.append((overlap, sent))

        scored.sort(reverse=True)

        return " ".join([s for _, s in scored[:top_k]])

    # CHECK ANSWER VALID
    def _is_valid_answer(self, answer, context):
        if not answer or len(answer.strip()) < 2:
            return False

        # answer phải nằm trong context
        if answer.lower() not in context.lower():
            return False

        return True

    # MAIN INFERENCE
    def __call__(self, question: str) -> str:
        if not question or not question.strip():
            return "I don't know"

        question = question.strip()

        # retrieve context
        context = self._retrieve_context(question)

        if not context:
            return "I don't know"

        results = self.qa_pipeline(
            question=question,
            context=context,
            top_k=3,
            max_answer_len=30,
            handle_impossible_answer=True
        )

        results = results if isinstance(results, list) else [results]

        threshold = self.config.confidence_threshold / 100.0

        best_answer = "I don't know"
        best_score = 0.0

        for res in results:
            ans = res.get("answer", "").strip()
            score = res.get("score", 0.0)

            if score < threshold:
                continue

            if not self._is_valid_answer(ans, context):
                continue

            if score > best_score:
                best_answer = ans
                best_score = score

        return best_answer