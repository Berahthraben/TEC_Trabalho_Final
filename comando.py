class Comando:
    def __init__(self, current_state, current_symbol, new_symbol, direction, new_state):
        self.current_state = current_state
        self.current_symbol = current_symbol
        self.new_symbol = new_symbol
        self.direction = direction
        self.new_state = new_state
    def printar(self):
        print("{} {} {} {} {}".format(str(self.current_state), self.current_symbol,
                                        self.new_symbol, self.direction, str(self.new_state)))
    def formatar(self):
        return "{} {} {} {} {}\n".format(
            self.current_state,
            self.current_symbol,
            self.new_symbol,
            self.direction,
            self.new_state,
            )
