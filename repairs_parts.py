import requests

import json
import os

"""[How to use the script]

the URL variable must be set in your bash prompt (see next line)
make sure that variable URL does not end with /
(YES: vroomly.com | NO : vroomly.com/)
export URL_TO_FETCH='https://www.vroomly.com/backend_challenge/labour_times'
export JSON_INPUT='data.json' #for the file input
export JSON_OUTPUT='quotations.json' #for the file output

"""

def exp_variables_from_bash():
    url_to_fetch = os.getenv("URL_TO_FETCH")
    json_input = os.getenv("JSON_INPUT")
    json_output = os.getenv("JSON_OUTPUT")
    return url_to_fetch, json_input, json_output

#url_to_fetch,json_input,json_output = exp_variables_from_bash()

def retrieve_hourly_rate(url_to_fetch, json_input):
    """retrieve_hourly_rate
    allows to retrieve the hourly rate from the APIetch
    input: url of the API, the json file given.
    output: dictionnary -> car_id,intervention_id,time spent
    """
    with open(json_input, "r") as jsonfile:
        json_data = json.load(jsonfile)
    cars = [
        json_data["cars"][val]["id"]
        for val in range(len(json_data["cars"]))]
    interventions = [
        json_data["interventions"][val]["id"]
        for val in range(len(json_data["interventions"]))
    ]
    spent_time_by_op_results = []
    for val_car in cars:
        for val_interv in interventions:
            results = requests.get(f"{url_to_fetch}/{val_car}/{val_interv}")
            #the json has to be in text format, hence the "results.text" below
            time_load = json.loads(results.text)
            time_load = time_load["labourTime"]
            spent_time_by_op_results.append(
                                            {"car_id": val_car,
                                             "interv_id": val_interv,
                                             "time_spent": time_load}
            )
    return spent_time_by_op_results


def services_charges(retrieve_hourly_rate, json_input):
    '''services_charges
    change the hourly rate to a rate per minute,
    for the workshops
    input: data from retrieve_hourly_rate
    output: dictionnary ->  car_id,
                            workshop_id,
                            price for the intervention,
                            intervention_id,
    '''
    with open(json_input, "r") as jsonfile:
        json_data = json.load(jsonfile)

    for val in range(len(json_data["workshops"])):
        json_data["workshops"][val]["hourly_rate"] = (
            float(json_data["workshops"][val]["hourly_rate"]) / 60
        )

    '''change the hh:mm:ss to a format with
     minutes e.g 1h20mn = 80mn
     '''
    for val_hour_rate in range(len(retrieve_hourly_rate)):
        hours, minutes, seconds = [
            int(i) for i in
            retrieve_hourly_rate[val_hour_rate]["time_spent"].split(":")
        ]
        total_minutes = hours * 60 + minutes
        retrieve_hourly_rate[val_hour_rate]["time_spent"] = total_minutes

    '''compute the prices for the intervention,
    per workshop according to the rates
    '''
    services_prices_per_workshop = []
    for val_workshop in range(len(json_data["workshops"])):
        for val_interv in range(len(retrieve_hourly_rate)):

            val_service = (
                retrieve_hourly_rate[val_interv]["time_spent"] *
                json_data["workshops"][val_workshop]["hourly_rate"]
            )
            services_prices_per_workshop.append(
                {
                    "car_id": retrieve_hourly_rate[val_interv]["car_id"],
                    "workshop_id": json_data["workshops"][val_workshop]["id"],
                    "intervention_id":
                        retrieve_hourly_rate[val_interv]["interv_id"],
                    "price_per_interv": val_service,
                }
            )
    return services_prices_per_workshop


def get_workshop_pref(services_charges_data):
    '''get_workshop_pref
    this function aim is is to add
    the preference of the workshop
    for the price part, either cheap, median or expensive
    input: dictionnary from the function services_charges
    output: same dictionnary with the preference of the workshop
    '''
    for val_work in range(len(services_charges_data)):
        if services_charges_data[val_work]["workshop_id"] == 1:
            services_charges_data[val_work]["preffered"] = "median"
        elif services_charges_data[val_work]["workshop_id"] == 2:
            services_charges_data[val_work]["preffered"] = "most_expensive"
        else:
            services_charges_data[val_work]["preffered"] = "cheapest"
    return services_charges_data


def get_part(part_type, car_id, preffered):
    """get_part
    allows you to find the best price part, according
    to the garage's preference.
    input: json file given acting as a database
    output: the price part, either cheap, median or
    expensive
    """
    with open(json_input, "r") as jsonfile:
        json_data = json.load(jsonfile)
    prices = sorted(
        [
            float(_["price"])
            for _ in json_data["parts"]
            if _["type"] == part_type and _["car_id"] == car_id
        ]
    )
    return (
        prices[0]
        if preffered == "cheapest"
        else prices[-1]
        if preffered == "most_expensive"
        else prices[int(len(prices) / 2)]
    )


def price_calculation(service_with_pref):
    """"price_calculation
    calculate the price part, according to the type
    if battery, just the price
    if pad or disc, the prices are front brake plus
    front pad, both are in pair.
    input: dictionnary from get_workshop_pref
    output: dictionnary with the part prices
    """
    for val in range(len(service_with_pref)):
        if service_with_pref[val]["intervention_id"] == 1:
            parts_price = get_part(
                "battery",
                service_with_pref[val]["car_id"],
                service_with_pref[val]["preffered"],
            )
            service_with_pref[val]["parts_price"] = parts_price
        else:
            parts_price = (
                get_part(
                    "front_brake_pad",
                    service_with_pref[val]["car_id"],
                    service_with_pref[val]["preffered"],
                ) * 2 +
                get_part(
                    "front_brake_disc",
                    service_with_pref[val]["car_id"],
                    service_with_pref[val]["preffered"],
                ) * 2
            )
            service_with_pref[val]["parts_price"] = parts_price
    return service_with_pref


def parts(services_charges_data, json_output):
    """parts
    change the intervention prices to a 2 digit, after decimal.


    input: dictionnary from price_calculation
    output: file, quotations.json, with a formatted dictionary.

    """
    for val in range(len(final_services_charges_data)):
        final_services_charges_data[val]["price_per_interv"] = "{:.2f}".format(
            final_services_charges_data[val]["price_per_interv"]
        )

    with open(json_output, "w") as jsonoutput:
        jsonoutput.write(json.dumps(services_charges_data,
                         sort_keys=True, indent=4))


if __name__ == "__main__":
    url_to_fetch, json_input, json_output = exp_variables_from_bash()
    retrieve_hourly_rate = retrieve_hourly_rate(url_to_fetch, json_input)
    services_charges_data = services_charges(retrieve_hourly_rate, json_input)
    service_with_preference = get_workshop_pref(services_charges_data)
    final_services_charges_data = price_calculation(service_with_preference)
    parts(final_services_charges_data, json_output)


""" expected output

    {
        "car_id": 1, ok
        "workshop_id": 1, ok
        "intervention_id": 1, ok
        "parts_price": "100.00",
        "services_price": "125.23" ok
    }


"""
