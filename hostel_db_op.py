from hostel_db import hostels

SHUFFLE_PREVIEW = True

# ImmutableMultiDict([('hostelType', 'PG-M'), ('distance', '100'), ('foodType', '0')])
def check(hostel_type,distance,with_food):
    # if hostel_type == "any" or distance == "any":
    #     pass
    # else 

    x = set()

    for i in hostels.keys():

        if distance != "any":

            if hostels[i]["survey"]["type"] == hostel_type and hostels[i]["survey"]["distance_below"] <= int(distance) and hostels[i]["survey"]["with_food"] == int(with_food):
                x.add(i)

        if distance == "any":
            if hostels[i]["survey"]["type"] == hostel_type and hostels[i]["survey"]["with_food"] == int(with_food):
                x.add(i)


    hostel_preview_dict = {}

    for i in list(x):
        hostel_preview_dict[i] = {}
        hostel_preview_dict[i]["name"] = hostels[i]["hostel_name"]
        hostel_preview_dict[i]["Preview"] = hostels[i]["Preview"]

    # print(json.dumps(hostel_preview_dict,indent=2))
    return hostel_preview_dict


# print(check(
#     hostel_type = "LH",
#     distance = "200",
#     with_food= "1"
#     ))


def fetch_all_preview():

    hostel_preview_dict = {}

    for i in hostels.keys():
        hostel_preview_dict[i] = {}
        hostel_preview_dict[i]["name"] = hostels[i]["hostel_name"]
        hostel_preview_dict[i]["Preview"] = hostels[i]["Preview"]


    if SHUFFLE_PREVIEW:

        import random

        items = list(hostel_preview_dict.items())
        random.shuffle(items)
        shuffled_dict = dict(items)

        return shuffled_dict

    else:
        
        # print(json.dumps(hostel_preview_dict,indent=2))
        return hostel_preview_dict
    # print(fetch_all_preview())
      

def fetch_details(id):


    hostel_details = hostels[id]["details"]
    hostel_details["hostel_id"] = id
    hostel_details["hostel_name"] = hostels[id]["hostel_name"]

    return hostel_details

    
def find_owner_phone_number(id):
    num = hostels[id]["more_details"]["owner"]["owner_wp"]

    return num if num else "nil"


def find_hostel_name(id):
    name = hostels[id]["hostel_name"]
    return name if name else "nil"

def find_hostel_gmap(id):
    
    coordinates = hostels[id]["more_details"]["hostel_gmap"] #[lat,long,markerloc-base64encoded]
    
    if len(coordinates) == 3:
        return coordinates
    else:
        return False

# print(find_hostel_gmap(2))
# print(find_hostel_name(1))
# print(json.dumps(fetch_details(2),indent=2))
# print(find_owner_phone_number(2))