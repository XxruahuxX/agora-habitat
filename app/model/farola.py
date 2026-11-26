class Farola:

    def __init__(self, id, encendida):
        self.id = id
        self.encendida = encendida

    def encender(self):
        if not self.encendida:
            self.encendida = True
            return True
        return False

    def apagar(self):
        if self.encendida:
            self.encendida = False
            return True
        return False

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["id"],
            d["encendida"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "encendida": self.encendida
        }
    