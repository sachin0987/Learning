
# def find_dict_with_value(list_of_dicts, search_string):
#     return next((d for d in list_of_dicts if any(search_string.lower() in v.lower() for v in d.values())), None)

# list_of_dicts = [
#     {'key1': 'test', 'key2': 'acb'},
#     {'key1': 'test1', 'key2': 'abc', 'key3': 'cbf'},
#     {'key1': 'test2', 'key2': 'def', 'key3': 'qwe'}
# ]

# search_value = 'abc'
# result_dict = find_dict_with_value(list_of_dicts, search_value)
# print(result_dict)
# if result_dict:
#     print(f"Dictionary containing '{search_value}' in a value: {result_dict}")
# else:
#     print(f"No dictionary found containing '{search_value}' in any value.")

def organize_dicts(list_of_dicts):
    try:
        result_dict = {}

        # Group dictionaries based on 'key1' values
        for dictionary in list_of_dicts:
            key1_value = dictionary.get('key1')
            if key1_value not in result_dict:
                result_dict[key1_value] = {key: [] for key in dictionary.keys() if key != 'key1'}

        # Populate values in the result dictionary and remove duplicates
        for dictionary in list_of_dicts:
            key1_value = dictionary.get('key1')
            for key, value in dictionary.items():
                if key != 'key1':
                    if key in result_dict[key1_value]:
                        if value not in result_dict[key1_value][key]:
                            result_dict[key1_value][key].append(value)
                    else:
                        result_dict[key1_value][key] = [value]

        # Remove empty lists from the result dictionary
        result_dict = {key: {k: v for k, v in value.items() if v} for key, value in result_dict.items()}

        return result_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
list_of_dicts = [
    {'key1': 'test', 'key2': 'acb'},
    {'key1': 'test1', 'key2': 'abc', 'key3': 'cbf'},
    {'key1': 'test', 'key2': 'def', 'key3': 'qwe'}
]

result = organize_dicts(list_of_dicts)
print(result)

def find_key(dictionary, key_to_find):
    if key_to_find in dictionary:
        return dictionary[key_to_find]
    else:
        return None  # Return None if key is not found

# Example dictionary
data = {
    'test': {'key2': ['acb', 'def'], 'key3': ['qwe']},
    'test1': {'key2': ['abc'], 'key3': ['cbf']}
}

# Key to search for
key = 'test1'

result = find_key(data, key)

if result is not None:
    print(f"The set for key '{key}' is: {result}")
else:
    print(f"Key '{key}' not found")

