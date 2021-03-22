# Input Sample
"""
    Create_parking_lot 6
    Park KA-01-HH-1234 driver_age 21
    Park PB-01-HH-1234 driver_age 21
    Slot_numbers_for_driver_of_age 21
    Park PB-01-TG-2341 driver_age 40
    Slot_number_for_car_with_number PB-01-HH-1234
    Leave 2
    Park HR-29-TG-3098 driver_age 39
    Vehicle_registration_number_for_driver_of_age 18
"""

# Output Sample
"""
    Created parking of 6 slots
    Car with vehicle registration number "KA-01-HH-1234" has been parked at slot number 1
    Car with vehicle registration number "PB-01-HH-1234" has been parked at slot number 2
    1,2
    Car with vehicle registration number "PB-01-TG-2341" has been parked at slot number 3
    2
    Slot number 2 vacated, the car with vehicle registration number "PB-01-HH-1234" left the space, the driver of the car was of age 21
    Car with vehicle registration number "HR-29-TG-3098" has been parked at slot number 2

"""


# Some Globals Vars
class Globals:
    last_parking_slot_no = 0
    parking_lot = {}
    parking_lot_size = 0
    vacated_slots = []


def create_park_adaptor(*args):
    # This will create the parking Lot.
    try:
        args = args[0]
        Globals.parking_lot_size = int(args[1])
        print(f'Created parking of {Globals.parking_lot_size} slots')
    except IndexError:
        print('Please define the Parking lot size')


def park_vehicle_adaptor(*args):
    # This will Park the parking Lot.
    try:
        args = args[0]
        vehicle_num = args[1]
        driver_age =  int(args[3])

        park_data = {
            "vehicle_number": vehicle_num,
            "driver_age": driver_age
        }

        # Check if any Vehicle has left and Slots are available in somewhere middle, Fill them first
        if Globals.vacated_slots:
            slot = Globals.vacated_slots.pop(0)
            Globals.parking_lot[slot] = park_data
            print(f'Car with vehicle registration number "{vehicle_num}" has been parked at slot number {slot}')
        else:
            Globals.last_parking_slot_no += 1   
            Globals.parking_lot[Globals.last_parking_slot_no] = park_data
            print(f'Car with vehicle registration number "{vehicle_num}" has been parked at slot number {Globals.last_parking_slot_no}')
    except Exception as e:
        print(f'Unable to Park Vehicle Due to - {e}')


def clear_slot_adaptor(*args):
    # This will clear the parking slot.
    try:
        args = args[0]
        slot_no = int(args[1])
        print(f'Slot number {slot_no} vacated, the car with vehicle registration number {Globals.parking_lot[slot_no]["vehicle_number"]} left the space, the driver of the car was of age {Globals.parking_lot[slot_no]["driver_age"]}')
        Globals.parking_lot[slot_no] = None
        Globals.vacated_slots.append(slot_no)
    except Exception as e:
        print(f'Error Occurred while Clearing Slot - {e}')    


def find_slots_by_age_adaptor(*args):
    # This will find the parking slots by driver age
    try:
        args = args[0]
        driver_age = int(args[1])
        slots = [ _index for _index in Globals.parking_lot.keys() if Globals.parking_lot[_index]['driver_age'] == driver_age]
        print(','.join(str(_x) for _x in slots))
    except Exception as e:
        print('null')

def find_slot_by_vehicle_no_adaptor(*args):
    # This will find the parking slots by Vehicle No
    try:
        args = args[0]
        vehicle_number = args[1]
        for _index in Globals.parking_lot.keys():
            if Globals.parking_lot[_index]['vehicle_number'] == vehicle_number:
                print(_index)
                break
    except Exception as e:
        print('null')

def find_vehicles_by_age_adaptor(*args):
    # This will find the Vehicle No's by Age
    try:
        args = args[0]
        driver_age = int(args[1])
        slots = [ Globals.parking_lot[_index]['vehicle_number'] for _index in Globals.parking_lot.keys() if Globals.parking_lot[_index]['driver_age'] == driver_age]
        print(','.join(str(_x) for _x in slots))
    except Exception as e:
        print('null')


if __name__ == '__main__':

    import sys

    # Orders and Actions mapping
    adaptor_factory = {
        "create_parking_lot": create_park_adaptor,
        "park": park_vehicle_adaptor,
        "slot_numbers_for_driver_of_age": find_slots_by_age_adaptor,
        "slot_number_for_car_with_number": find_slot_by_vehicle_no_adaptor,
        "vehicle_registration_number_for_driver_of_age": find_vehicles_by_age_adaptor,
        "leave": clear_slot_adaptor
    }

    """
        Example Parking slot Database using Nested Dicts:
        {
            1:  {
                    "vehicle_number": "KA-01-HH-1234"
                    "driver_age": 21
                },
            2:  {
                    "vehicle_number": "PB-01-TG-2341"
                    "driver_age": 40
                },
        }
    """

    # Check if File Path is provided or not.
    if len(sys.argv) < 2:
        print("No Input File Path defined.")
        exit()

    # Read File Input
    _file = open(sys.argv[1])

    for _line in _file.readlines():
        if adaptor_factory.get(_line.split()[0].lower()):
            _func = adaptor_factory.get(_line.split()[0].lower())
            _func(_line.split())
        else:
            print(f"There is some issue with the input. Please Fix the Input - {_line}")
            exit()
