import re

def parse_acl_config(acl_config, acl_names=None):
    acl_pattern = re.compile(r"ip access-list (?:standard|extended) (\S+)\s*\n((?:\s+ \d+ )?(?: .*\n)+)") 

    acls = {}
    for acl_match in acl_pattern.finditer(acl_config):
        acl_name = acl_match.group(1)
        if acl_names is None or acl_name in acl_names:
            aces = acl_match.group(2).strip().split("\n")
            print(aces)
            aces = [re.sub(r"^\s+\d+\s+", "", ace) for ace in aces]
            acls[acl_name] = aces
    if acl_names is not None:
        for acl_name in acl_names:
            if acl_name not in acls:
                acls[acl_name] = []

    return acls


acl_config = """
ip access-list extended ACL_1 
  10 permit tcp 192.168.1.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 80
  20 permit udp 192.168.1.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 53
  30 deny ip any any
  40 permit udp host 10.10.10.1 any
!
ip access-list extended ACL_2
  permit tcp any any
  deny ip any any

ip access-list standard ACL_3
  permit icmp any any
"""

acls = parse_acl_config(acl_config, acl_names=["ACL_1","ACL_4"])
print(acls)