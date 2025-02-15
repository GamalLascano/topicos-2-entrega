import torch
from pykeen.triples import TriplesFactory

class PredictionService:
    triples_dataset = 'data/triples_dataset.pkl'
    trained_model = 'data/trained_model.pkl'
    same_as_relation = 'http://www.w3.org/2002/07/owl#sameAs'
    def __init__(self):
        self.model = torch.load(trained_model, weights_only=False) if torch.cuda.is_available() else torch.load(trained_model, map_location=torch.device('cpu'), weights_only=False)
        self.triples_factory = TriplesFactory.from_path(triples_file, create_inverse_triples=True)
        pd.read_csv(triples_file, sep='\t', header=None, names=['head', 'relation', 'tail'])

    def predict(self, originalProperty, comparedProperty):
        head_idx = [self.triples_factory.entity_to_id[originalProperty]]
        relation_idx = [self.triples_factory.relation_to_id[same_as_relation]]

        entityBase = torch.tensor(list(zip(head_idx,relation_idx)))
        scores = self.model.score_t(entityBase)
        score = scores[0][self.triples_factory.entity_to_id[comparedProperty]]

        return score.item()
        