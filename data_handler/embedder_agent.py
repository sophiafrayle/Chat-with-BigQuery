from abc import ABC
from vertexai.language_models import TextEmbeddingModel

class EmbedderAgent(ABC):
    """
    This Agent generates embeddings.
    """
    agentType: str = "EmbedderAgent"

    def __init__(self, mode, embeddings_model='textembedding-gecko@002'):
        if mode == 'vertex':
            self.mode = mode
            self.model = TextEmbeddingModel.from_pretrained(embeddings_model)
        else:
            raise ValueError('EmbedderAgent mode must be vertex')

    def create(self, question):
        """Text embedding with a Large Language Model."""

        if self.mode == 'vertex':
            if isinstance(question, str):
                embeddings = self.model.get_embeddings([question])
                for embedding in embeddings:
                    vector = embedding.values
                return vector

            elif isinstance(question, list):
                vector = []
                for q in question:
                    embeddings = self.model.get_embeddings([q])

                    for embedding in embeddings:
                        vector.append(embedding.values)
                return vector

            else:
                raise ValueError('Input must be either str or list')
