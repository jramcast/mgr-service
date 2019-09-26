from ... import domain

class NaiveBayesInputFeatures(domain.entities.ModelInputFeatures):
    pass

class NaiveBayesModel(domain.interfaces.Model):

    def predict(self, features: NaiveBayesInputFeatures):
        
