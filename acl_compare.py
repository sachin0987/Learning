def compare_acl(current_acl, expected_acl):
    differences = {}
    status = False

    all_acl_keys = set(current_acl.keys()).union(expected_acl.keys())

    for acl_name in all_acl_keys:
        set_current_acl = {line.strip() for line in current_acl.get(acl_name, [])}
        set_expected_acl = {line.strip() for line in expected_acl.get(acl_name, [])}

        if set_current_acl != set_expected_acl:
            missing_values = list(set_expected_acl - set_current_acl)
            extra_values = list(set_current_acl - set_expected_acl)

            differences[acl_name] = {
                "missing_in_current_acl": missing_values,
                "extra_in_current_acl": extra_values
            }
            status = True

    return status, differences

# Example ACLs in CLI form with extra spaces in lines
current_acl = {
    "ACL_1": [
        " permit tcp 192.168.1.0/24 10.0.0.0/24 eq 80",
        " permit udp 192.168.1.0/24 10.0.0.0/24 eq 53",
        "deny ip any any ",
        " permit udp 10.10.10.1  "
    ],
    "ACL_2": [
        "permit tcp any any ",
        "deny ip any any  "
    ],
    "ACL_3": [
        " permit icmp any any"
    ]
}

expected_acl = {
    "ACL_1": [
        "permit tcp 192.168.1.0/24 10.0.0.0/24 eq 80",
        "permit udp 192.168.1.0/24 10.0.0.0/24 eq 53",
        "permit icmp any any",
        "deny ip any any",
        "permit udp 10.10.10.1"
    ],
    "ACL_2": [
        "deny tcp any any",
        "deny ip any any"
    ],
    "ACL_4": [
        "permit udp any any"
    ]
}

# Function call and printing the status along with differences
status, differences = compare_acl(current_acl, expected_acl)

print("Status:", "ACLs have differences" if status else "ACLs are equal")

if status:
    print("\nDifferences:")
    for acl_name, values in differences.items():
        print(f"\nACL Name: {acl_name}")
        if values['missing_in_current_acl']:
            print("Missing in current ACL:", values['missing_in_current_acl'])
        if values['extra_in_current_acl']:
            print("Extra in current ACL:", values['extra_in_current_acl'])
