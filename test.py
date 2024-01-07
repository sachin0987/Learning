import json

with open("test.json", "rb") as f:
    json_data = json.load(f)

json_list = (json_data.get("TABLE_vrf")).get("ROW_vrf")

test_list =[]
for ip_route in json_list:
    test_dict = {"VRF":None,"SUBNET":None,"GATEWAY":None,"INTERFACE":None,"METRIC":None}
    VRF = ip_route.get("vrf-name-out")
    route_info = ip_route["TABLE_addrf"]["ROW_addrf"]["TABLE_prefix"]["ROW_prefix"]
    for routes in route_info:
        test_dict["VRF"] = VRF
        test_dict["SUBNET"] = routes.get("ipprefix")
        table_path = routes["TABLE_path"]["ROW_path"]
        if type(table_path) is list:
            for table_prifix in table_path:
                print(table_path)
                test_dict["GATEWAY"] = table_prifix.get("ipnexthop")
                test_dict["INTERFACE"] = table_prifix.get("ifname")
                test_dict["METRIC"] = table_prifix.get("metric")
        else:
            test_dict["GATEWAY"] = table_path.get("ipnexthop")
            test_dict["INTERFACE"] = table_path.get("ifname")
            test_dict["METRIC"] = table_path.get("metric")
        test_list.append(test_dict)

print(test_list)

# # Function to remove specified keys while keeping values intact
def remove_keys(json_obj, keys_to_remove):
    if isinstance(json_obj, dict):
        new_dict = {}
        for key, value in json_obj.items():
            if key in keys_to_remove:
                continue
            if isinstance(value, dict):
                new_dict[key] = remove_keys(value, keys_to_remove)
            else:
                new_dict[key] = value
        return new_dict
    elif isinstance(json_obj, list):
        return [remove_keys(item, keys_to_remove) for item in json_obj]
    else:
        return json_obj

# Specify the keys to remove
keys_to_remove = ["TABLE_path", "ROW_path"]

# Remove the specified keys while keeping values intact
cleaned_json = remove_keys(input_json, keys_to_remove)

# # Print the cleaned JSON
# import json
# print(json.dumps(cleaned_json, indent=4))
