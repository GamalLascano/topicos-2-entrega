import torch
import pandas as pd
import numpy as np
from pykeen.triples import TriplesFactory

class PredictionService:
    triples_dataset = 'prediction/model/triples_dataset.tsv.gz'
    trained_model = 'prediction/model/trained_model.pkl'
    same_as_relation = 'http://www.w3.org/2002/07/owl#sameAs'

    def __init__(self):
        self.model = torch.load(self.trained_model, weights_only=False) if torch.cuda.is_available() else torch.load(self.trained_model, map_location=torch.device('cpu'), weights_only=False)
        self.triples_factory = TriplesFactory.from_path(self.triples_dataset, create_inverse_triples=True)
        pd.read_csv(self.triples_dataset, sep='\t', header=None, names=['head', 'relation', 'tail'])

    def predict(self, originalProperty:int, comparedProperty) -> np.float64:
        head_idx = [originalProperty]
        relation_idx = [self.triples_factory.relation_to_id[self.same_as_relation]]

        entityBase = torch.tensor(list(zip(head_idx,relation_idx)))
        scores = self.model.score_t(entityBase)
        score = scores[0][comparedProperty]
        return -score.item()