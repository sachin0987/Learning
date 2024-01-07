from ncclient import manager
import xml.dom.minidom

nc_conn = manager.connect(
    host="sandbox-iosxr-1.cisco.com",
    port=22,
    username="admin",
    password="C1sco12345",
    hostkey_verify=False,
)
# for capability in log_router.server_capabilities:
#    print (capability)
nc_config = nc_conn.get_config(source='running').data_xml
print(nc_config)
# hostname_filter = """
#                       <filter>
#                           <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-snmp-agent-cfg">
#                           </native>
#                       </filter>
#                 """
# # Pretty print the XML reply
# xmlDom = xml.dom.minidom.parseString(
#     str(log_router.get_config("running", hostname_filter))
# )
# print(xmlDom.toprettyxml(indent="  "))
