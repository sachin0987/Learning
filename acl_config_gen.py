def create_config(acl_dict):
    """
    This function takes a dictionary containing ACL information as input and returns a string containing the configuration
    commands.

    Args:
        acl_dict (dict): A dictionary containing ACL information.

    Returns:
        str: A string containing the configuration commands.
    """
    fixes = rollback = ""
    for acl_name in acl_dict.keys():
        # Add the ACL name to the configuration
        fixes += f"ip access-list extended {acl_name}\n"
        rollback += f"ip access-list extended {acl_name}\n"
        # Remove the unwanted entries from the configuration
        if "unwanted" in acl_dict[acl_name]:
            for unwanted_conf in acl_dict[acl_name]["unwanted"]:
                fixes += f"  no {unwanted_conf}\n"
                rollback += f"  {unwanted_conf}\n"
        # Add the missing entries to the configuration
        if "missing" in acl_dict[acl_name]:
            for missing_conf in acl_dict[acl_name]["missing"]:
                fixes += f"  {missing_conf}\n"
                rollback += f"  no {missing_conf}\n"

    return fixes,rollback

# Example usage
acl_dict = {"ACL_1":{"missing":['permit tcp host 10.10.1.1','permit tcp host 10.10.1.2'],"unwanted":['permit tcp host 127.10.1.1','permit tcp host 123.10.1.3']},\
            "ACL_2":{"missing":['permit tcp host 10.10.1.1/24','permit tcp host 10.10.1.7'],"unwanted":[]}}
fixes,rollback = create_config(acl_dict)
print(fixes)
print(rollback)


