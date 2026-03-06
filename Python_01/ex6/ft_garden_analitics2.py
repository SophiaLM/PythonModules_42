#!/usr/bin/env python3

# Clase base que hara de padre
# Type_id: no podemos usar duck typing, ni ninguna funcion
# que reconozca cada hijo de su padre, puesto que para:
# Plant types: 1 regular, 1 flowering, 1 prize flowers y para
# cumplir con lo siguiente: Each garden should track plant collections
# and statistics; deberemos manejar los datos de esas plantas

class Plant:
    type_id = 0

    def __init__(self, name, height):
        self.name = name
        self.height = height

    def grow(self):  # Metodo de instancia! modifica estado de height
        self.height += 1
        print(f"{self.name} grew 1cm")

    # Metodo de instancia! la base, lo mejoraremos con las clases hijas
    def get_info(self):
        return f"{self.name}: {self.height}cm"


# Primer hijo, agregamos los datos de plant con super
class FloweringPlant(Plant):
    type_id = 1

    def __init__(self, name, height, color):
        super().__init__(name, height)
        self.color = color

    # Polimorfismo? llamo a la informacion de get_info original
    # Y agrego aquello nuevo que necesito (grande el super)
    def get_info(self):
        return f"{super().get_info()}, {self.color} flowers (blooming)"


# Repetimos
class PrizeFlower(FloweringPlant):
    type_id = 2

    def __init__(self, name, height, color, pts):
        super().__init__(name, height, color)
        self.pts = pts

    def get_info(self):
        return f"{super().get_info()}, Prize points: {self.pts}"


# CLASE GARDEN gestion de datos individuales del jardin
class Garden:
    def __init__(self, owner):
        self.owner = owner
        self.plants = []   # Lista de plantas del jardin
        self.added = 0
        self.total_growth = 0

    def add_plant(self, plant):
        # Concatenacion, como mi str_append
        self.plants = self.plants + [plant]
        self.added += 1
        print(f"Added {plant.name} to {self.owner}'s garden")

    # P se crea automaticamente con cada vuelta del bucle,
    # Basicamente ejecuta la funcion en cada planta
    def grow_all(self):
        print(f"{self.owner} is helping all plants grow...")
        for p in self.plants:
            p.grow()
            self.total_growth += 1


# ===EMPEZAMOS GARDEN MANAGER===#

# Manager y helper == manejamos el numero de plantas y cuanto crecieron.
# Definimos un molde para el dueño del jardin, y numero de jardines
# Definimos GardenStats(subject) que sera un helper
# (maneja una tarea secundaria)
# Definimos el metodo statico count_types, donde usaremos el id para
# reconocer el tipo de planta y marcarla con un numero
# Ahora si inicializamos, agregamos los jardines

class GardenManager:
    total_gardens = 0

    class GardenStats:
        def __init__(self, plants):
            self.plants = plants

        @staticmethod
        def count_types(plants):
            r = 0
            f = 0
            pf = 0
            for p in plants:
                if p.type_id == 0:
                    r += 1
                elif p.type_id == 1:
                    f += 1
                elif p.type_id == 2:
                    pf += 1
            return r, f, pf

        @staticmethod
        def garden_score(plants):
            score = 0
            for p in plants:
                score += p.height
                if p.type_id == 2:
                    score += p.pts * 2
            return score

    def __init__(self):
        self.gardens = []

    def add_garden(self, garden):
        self.gardens = self.gardens + [garden]
        GardenManager.total_gardens += 1

    @classmethod
    def create_garden_network(cls):
        return cls.total
