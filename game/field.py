MAX_MINION = 5
FIELD_FULL_MESSAGE = "Your field is full."


class Field:
    def __init__(self):
        self.minions = []

    def is_full(self):
        return len(self.minions) >= MAX_MINION

    def add_minion(self, minion):
        if self.is_full():
            return [FIELD_FULL_MESSAGE]

        self.minions.append(minion)
        return [f"{minion.name} entered the field."]

    def remove_dead_minions(self):
        messages = []
        alive_minions = []

        for minion in self.minions:
            if minion.health <= 0:
                messages.append(f"{minion.name} died.")
            else:
                alive_minions.append(minion)

        self.minions = alive_minions
        return messages

    def get_display_text(self):
        if not self.minions:
            return "Empty"

        result = []
        for index, minion in enumerate(self.minions, start=1):
            status = "Exhausted" if minion.has_attacked else "Ready"
            result.append(
                f"{index}. {minion.name} "
                f"({minion.attack}/{minion.health}) {status}"
            )

        return "\n".join(result)
