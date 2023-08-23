class Messenger:
    def __init__(self):
        self.messages = []
        self.admin_messages = []
        self.info = []
        self.warnings = []
        self.errors = []

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def add_info(self, message):
        self.info.append(message)

    def get_info(self):
        return self.info

    def add_warning(self, message):
        self.warnings.append(message)

    def get_warnings(self):
        return self.warnings

    def add_error(self, message):
        self.errors.append(message)

    def get_errors(self):
        return self.errors

