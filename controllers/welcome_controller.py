from models.welcome_model import WelcomeModel

class WelcomeController:
    """
    Controller for welcome page
    """

    def __init__(self, model=None):
        self.model = model or WelcomeModel()

    def get_title(self):
        return "Welcome"
