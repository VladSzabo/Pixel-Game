from general.Constants import Constants


class Message:

    timer = 0

    def __init__(self, text, font, color, x, y, display_time=300):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.display_time = display_time
        self.surface = self.font.render(text, 1, color)

    def render(self, game_display):
        game_display.blit(self.surface, [self.x, self.y])
        self.timer += 1

    def get_height_text(self):
        return self.font.size(self.text)


class Messages:
    messages = []
    test_message = None

    def __init__(self):
        Messages.test_message = Message("This is a test", Constants.fonts["font1"], (0, 0, 0), 0, 0)

    @staticmethod
    def render(game_display):
        c = 0
        while c < len(Messages.messages):
            Messages.messages[c].render(game_display)
            if Messages.messages[c].timer > Messages.messages[c].display_time:
                Messages.messages.pop(c)
            c += 1

    @staticmethod
    def add_message(message_text):
        for message in Messages.messages:
            message.y -= Messages.test_message.get_height_text()[1]

        Messages.messages.append(
            Message(message_text, Constants.fonts["font1"], (20, 20, 20), 0,
                    Constants.height - Messages.test_message.get_height_text()[1])
        )
