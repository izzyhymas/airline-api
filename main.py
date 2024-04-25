from fastapi import FastAPI

import json

from models import Flight, AirlineName


app = FastAPI()

with open("airlines.json", "r") as f:
    flight_dict: dict = json.load(f)

flights: dict[AirlineName, list[Flight]] = {}
for airline_name, flight_list in flight_dict.items():
    airlines = AirlineName(airline_name)
    value: list[Flight] = []
    for flight in flight_list:
        value.append(Flight(**flight))
    flights[airlines] = value


# GET / -> list[airline_name]
@app.get("/airlines")
async def get_airlines() -> list[AirlineName]:
    return list(flights.keys())

# GET /:airline_name -> list[flight_num]
@app.get("/{airline_name}")
async def get_airline_flights(airline_name: str) -> list[str]:
    airline = AirlineName(airline_name)
    if airline in flights:
        flight_nums = []
        for flight in flights[airline]:
            flight_nums.append(flight.flight_num)
        return flight_nums
    
# GET /:airline_name/:flight_num -> Flight
@app.get("/{airline_name}/{flight_num}")
async def get_flight(airline_name: str, flight_num: str) -> Flight:
    airline = AirlineName(airline_name)
    if airline in flights:
        for flight in flights[airline]:
            if flight.flight_num == flight_num:
                return flight

# POST /:airline
@app.post("/{airline}")
async def create_flight(airline: str, flight: Flight) -> None:
    airline_name = AirlineName(airline)
    if airline_name in flights:
        flights[airline_name].append(flight)
    else:
        flights[airline_name] = [flight]
       
# PUT /:airline/:flight_num
@app.put("/{airline}/{flight_num}")
async def update_flight(airline: str, flight_num: str, updated_flight: Flight) -> None:
    airline_name = AirlineName(airline)
    if airline_name in flights:
        for i, flight in enumerate(flights[airline_name]):
            if flight.flight_num == flight_num:
                flights[airline_name][i] = updated_flight
                return

# PATCH /:airline/:flight_num
@app.patch("/{airline}/{flight_num}")
async def patch_flight(airline: str, flight_num: str, updated_capacity: int) -> None:
    airline_name = AirlineName(airline)
    if airline_name in flights:
        for flight in flights[airline_name]:
            if flight.flight_num == flight_num:
                flight.capacity = updated_capacity
                return

# DELETE /:airline/:flight_num
@app.delete("/{airline}/{flight_num}")
async def delete_flight(airline: str, flight_num: str) -> None:
    airline_name = AirlineName(airline)
    if airline_name in flights:
        updated_flight = []
        for flight in flights[airline_name]:
            if flight.flight_num != flight_num:
                updated_flight.append(flight)
        flights[airline_name] = updated_flight