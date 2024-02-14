ACME backend challenge
-------------------------

## Guidelines

NB: I've used the library requests. There is a file `requirements.txt` to install it with pip 

## Statement

We are building a car maintenance quotation generator.

The goal is to be able to find the parts and services prices
that a car owner would pay for a given intervention at a given workshop.
Example: how much would it cost to change the front break pads of a
Renault Clio III 1.5dCi 68cv at Speedy Bègles?

### Services
The services price is computed as 

- the number of hours of labour required to perform the
intervention on the car 

multiplied 

- by the hourly price the workshop is charging.

The labour times are not a constant of the intervention, they vary from car
to car. We use the help of an external service to retrieve labour times for a given
intervention and a given car.
 
We setup an API endpoint that you can use to retrieve those in the context of the exercise.
 
To use it make a GET HTTP request to `https://www.vroomly.com/backend_challenge/labour_times/<car_id>/<intervention_id>/`
where 
- `<car_id>` (1 = 'Peugeot 307 CC', 2 = 'BMW Série 3', 3 = 'Toyota Rav 4 3' )  
- `<intervention_id>` should be replaced by corresponding values. (1 = 'Changement de la batterie', 2 = 'Changement des disques et plaquettes avant')

Note: the format of the labour times is the following: `hh:mm:ss`

### Parts
The parts price is the sum of the prices of the parts being replaced during the intervention.

For each intervention: 

we know 

- The count : the type of parts that need to be changed
(example for a front brake pads change, 2 front brake pads need to be changed).

- Multiple parts may be used interchangeably at a given position for a given car.

(example: when changing your front brake pads, you may use Ferodo pads or
the more expensive Bosch ones.)

- To allow us to compute a fixed parts price, we ask the workshop owners
  to tell us whether they want us to use the price of 
 - the cheapest
 - the median
 - the most expensive part. 
 This choice is stored as an enum under the `preferred_part_price` key.
 Its possible values are `cheapest`, `median`, `most_expensive`.



## Expected output

Your input data is present in `data.json`, write code that generates a `quotations.json`
file containing a list of the quotations for each car, each intervention and each workshop.
A quotation should have the following structure:

    {
        "car_id": 1,
        "workshop_id": 1,
        "intervention_id": 1,
        "parts_price": "100.00",
        "services_price": "125.23"
    }
