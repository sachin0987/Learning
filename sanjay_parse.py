import time
import textfsm
from jumpssh import SSHSession
import pandas as pd


def execute_commands(session, commands):
    outputs = []
    for cmd in commands:
        output = session.get_cmd_output(cmd)
        outputs.append(output)
    return outputs

def ssh_with_jump_host(jump_host, target_host, jump_user, jump_pwd, target_user, target_pwd, commands):
    max_retries = 3
    retry_count = 0
    connected = False

    while not connected and retry_count < max_retries:
        outputs = []
        try:
            # Establish SSH session via jump host
            gateway_session = SSHSession(jump_host, jump_user, password=jump_pwd).open()
            # Connect to the target host from the jump host
            target_session = gateway_session.get_remote_session(target_host, target_user, password =target_pwd)
            # Execute commands on the target host
            outputs = execute_commands(target_session, commands)

            # Close the SSH sessions
            target_session.close()
            gateway_session.close()

            connected = True  # Set connected to True on successful execution
        except EOFError as eof_err:
            print(f"EOF error: {eof_err}")
            retry_count += 1
            print(f"Reconnecting... Attempt {retry_count}")
            time.sleep(2)  # Wait for a few seconds before attempting reconnection
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Exit the loop on other exceptions

        finally:
            return outputs
        
    if not connected:
        print("Connection failed after retries.")

# Example usage for executing multiple commands via jump host
# Define jump server (gateway) details
jump_host = '192.168.15.71'
jump_user = 'dcn'
jump_pwd = 'Challenges@1'

# Define target node details
target_host = '192.168.20.15'
target_user = 'snanda'
target_pwd = 'Markona#159703'

commands_to_execute = [
    "terminal length 0",
    "show vrf all detail"
]


vrf_output = ssh_with_jump_host(jump_host, target_host, jump_user, jump_pwd, target_user, target_pwd, commands_to_execute)
# Display the output of the "show version" command
print(vrf_output)

# Define the raw output from 'show vrf all details' command (replace this with your actual output)

def parse_vrf_details(raw_output):
    template_file = open('vrf_template.template', 'r')
    template = textfsm.TextFSM(template_file)
    # Parse the raw output using TextFSM
    parsed_output = template.ParseText(raw_output)
    vrfs = []
    for entry in parsed_output:
        vrfs.append(entry[0])
    return vrfs


print(parse_vrf_details(vrf_output))
vrf_list=parse_vrf_details(vrf_output)

def ip_route_parse(vrfname,ip_route_output):
    template_file = open('ip_route.template', 'r')
    template = textfsm.TextFSM(template_file)
    parsed_output = template.ParseText(ip_route_output)
    # print(parsed_output) 
    ip_routes = []
    for i in parsed_output:
        if i[0] == "via":
            ip_routes.append(i[1])
    ip_routes=list(set(ip_routes))
    return {"vrf":vrfname, "ip_routes":ip_routes}
    
vrf_route_output_list = []
vrf_cmds = []

for vrf in vrf_list:
    vrf_cmds.append(f'show route vrf {vrf}')
vrf_route_output = ssh_with_jump_host(jump_host, target_host, jump_user, jump_pwd, target_user, target_pwd, commands_to_execute)

for raw_output in vrf_route_output:
    vrf_route_output_list.append(ip_route_parse(vrf,raw_output))

print(vrf_route_output_list)

def check_sr_pfx(vrfname,prx,raw_output):
    template_file = open('sr_pfx.template', 'r')
    template = textfsm.TextFSM(template_file)
    parsed_output = template.ParseText(raw_output)
    resp_list = sum(parsed_output, [])
    if len(set(resp_list)) == 1:
        resp_dict = {"vrf":vrfname, "sr_pfx":prx,"status":"Pass"}
        
    else:
        resp_dict = {"vrf":vrfname, "sr_pfx":prx,"status":"Fail"}
    return resp_dict

print(vrf_route_output_list)
vrf_details_list=[]
for vrf_details in vrf_route_output_list:
    if len(vrf_details["ip_routes"]) > 0:
        for route in vrf_details["ip_routes"]:
            print(f'show mpls forwarding prefix {route}/32')
            sr_pfx_resp = remote_session.get_cmd_output(f'show mpls forwarding prefix {route}/32')
            time.sleep(1)
            print(sr_pfx_resp)
            vrf_details_list.append(check_sr_pfx(vrf_details["vrf"],route,sr_pfx_resp))
    else:
        vrf_details_list.append({vrf:vrf_details["vrf"],"sr_pfx":"N/A","status":"N/A"})

print(vrf_details_list)
vrf_df = pd.DataFrame(vrf_details_list)
print(vrf_df)