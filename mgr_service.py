from service.server import serve

from service.languages.controller import LanguagesController
from service.languages.repository import LanguagesInMemoryRepository
from service.languages.infrastructure import BabelLanguagesLocalizer

from service.currencies.controller import CurrenciesController
from service.currencies.repository import CurrenciesInMemoryRepository
from service.currencies.infrastructure import BabelCurrenciesLocalizer

from service.boards.controller import BoardsController
from service.boards.repository import BoardsJsonFileRepository

from service.categories.controller import CategoriesController
from service.categories.repository import CategoriesJsonFileRepository

languages_repository = LanguagesInMemoryRepository()
languages_translator = BabelLanguagesLocalizer()
languages_controller = LanguagesController(
    languages_repository, languages_translator
)

currencies_repository = CurrenciesInMemoryRepository()
currencies_translator = BabelCurrenciesLocalizer()
currencies_controller = CurrenciesController(
    currencies_repository, currencies_translator
)

boards_repository = BoardsJsonFileRepository()
boards_controller = BoardsController(boards_repository)

categories_repository = CategoriesJsonFileRepository()
categories_controller = CategoriesController(categories_repository)

serve(
    languages_controller,
    currencies_controller,
    boards_controller,
    categories_controller
)
