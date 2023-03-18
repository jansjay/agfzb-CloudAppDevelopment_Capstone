from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    address = models.TextField()
    def __str__(self):
        return self.name + " " + self.description + " " + self.address


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    name = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    year = models.IntegerField()
    car_make = models.ForeignKey(CarMake,null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.type + ", Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    #       E.g.  "id": 1,
    #             "city": "El Paso",
    #             "state": "Texas",
    #             "st": "TX",
    #             "address": "3 Nova Court",
    #             "zip": "88563",
    #             "lat": 31.6948,
    #             "long": -106.3,
    #             "short_name": "Holdlamis",
    #             "full_name": "Holdlamis Car Dealership"
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name
    def __str__(self):
        return "Dealer id: " + self.id + ", Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    #      E.g   "name": "Berkly Shepley",
    #            "dealership": 15,
    #            "review": "Total grid-enabled service-desk",
    #            "purchase": true,
    #            "purchase_date": "07/11/2020",
    #            "car_make": "Audi",
    #            "car_model": "A6",
    #            "car_year": 2010
    #            "sentiment" -> calculated
    def __init__(self, id, name, dealership, purchase, review, purchase_date, car_make, car_model, car_year, sentiment):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review id: " + self.id + ", Name: " + self.name +  ", Review: " + self.review 