import random
import math
import datetime
from os import system


class SA:
    def __init__(self, iterations, temp, alpha):
        self.iterations = iterations
        self._temp = temp
        self.alpha = alpha

    def easom(self, x1, x2):
        easom = -math.cos(x1)*math.cos(x2) * \
            math.exp(-(x1-math.pi)**2-(x2-math.pi)**2)
        return easom

    def shift(self, x1, x2):
        temp = self.get_temperature()
        delta1 = temp * random.uniform(-1, 1)
        delta2 = temp * random.uniform(-1, 1)
        xnew = x1 + delta1
        xprev = x2 + delta2
        easom_value = self.easom(xnew, xprev)
        return [easom_value, xnew, xprev]

# Gettery

    def get_temperature(self):
        return self._temp

    def get_difference(self, new_solution, current_solution):
        return new_solution - current_solution

    def get_random_solution(self):
        x1 = random.randint(-100, 100)
        x2 = random.randint(-100, 100)
        easom_value = self.easom(x1, x2)
        return [easom_value, x1, x2]

    def get_probability(self, point1, point2):
        temp = self.get_temperature()
        prob = random.uniform(0, 1)
        delta = self.get_difference(point1[0], point2[0])

        if prob < math.exp(- delta/temp):
            return point1
        else:
            return point2

    def get_solution(self):
        start = datetime.datetime.now()
        randomPoint = self.get_random_solution()  # x0
        temp = self.get_temperature()

        for i in range(0, self.iterations):
            randomNew = self.shift(randomPoint[1], randomPoint[2])  # x1

            if randomPoint[0] > randomNew[0]:
                randomPoint = randomNew

            if randomPoint[0] < randomNew[0]:
                randomPoint = self.get_probability(randomPoint, randomNew)

            temp = temp * self.alpha

        duration = datetime.datetime.now() - start
        return randomPoint, duration


def main():
    try:
        iterations = int(input("Podaj ilosc iteracji: "))
        temp = int(input("Podaj temperature poczatkowa: "))
        alpha = float(
            input("Podaj zmiane temperatury (ulamek z zakresu od 0.8 do 0.99): "))
        if alpha <= 0.7 or alpha >= 1:
            raise ValueError(
                "Blad zakresu! Podana liczba musi byc wieksza od 0 i mniejsza od 1")
    except ValueError:
        print("Podano niepoprawna wartosc!")

    sa = SA(iterations, temp, alpha)
    solution, duration = sa.get_solution()
    system("cls")
    print('Wybrane parametry:')
    print(f'Ilosc iteracji: {iterations}')
    print(f'Temperatura: {temp}')
    print(f'Zmiana temperatury: {alpha}')
    print(f'Minimum globalne funkcji Easoma to: {solution[0]}')
    print(f'W punktach x1 = {solution[1]}, x2 = {solution[2]}')
    print(f'Znalezione w czasie: {duration}')


if __name__ == "__main__":
    main()
