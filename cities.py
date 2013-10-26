import csv
import re
import bisect

class Cities:

    def __init__(self):
        self._city_to_population = {}
        self._population_to_city = {}
        self._populations = []

        no_digits_re = re.compile('[^\d]')

        with open('data/cities.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                city = row[0]
                population = int(no_digits_re.sub("", row[4]))

                self._city_to_population[city] = population
                self._populations.append(population)
                if population in self._population_to_city:
                    self._population_to_city[population].append(city)
                else:
                    self._population_to_city[population] = [city]

            self._populations.sort()

    def get_population_for_city(self, city):
        return self._city_to_population[city]
    
    def get_some_city_for_population(self, population):
        return self._population_to_city[population][0]
            
    def get_similar_city(self, city):
        population = self.get_population_for_city(city)

        if len(self._population_to_city[population]) > 1:
            # We could easily do without this loop, but hopefully there won't be too many
            # cities with the same population 
            for other_city in self._population_to_city[population]:
                if other_city != city:
                    # Other city with exactly the same population exists 
                    return other_city
        else:
            index = bisect.bisect_left(self._populations, population)
            if index > 0:
                return self.get_some_city_for_population(self._populations[index - 1])
            else:
                return self.get_some_city_for_population(self._populations[index + 1])



