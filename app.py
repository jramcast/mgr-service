from mgr.infrastructure.server.flask import Server
from mgr.usecases.predict import ClassifyUseCase
from mgr.infrastructure.models.naivebayes import NaiveBayesModel


naive_bayes = NaiveBayesModel()

predict_usecase = ClassifyUseCase(naive_bayes)

server = Server(predict_usecase)
app = server.serve()
