
from configparser import ConfigParser
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import  Message
from MiFloraData import MiFloraData

import asyncio
import random
import uuid
import json


# PROVISION DEVICE
async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )
    return await provisioning_device_client.register()



async def send_telemetry(device_client, message):
    try:
        print("Sending telemetry for temperature")   
        msg = Message(message)
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"

        await device_client.send_message(msg)

    except Exception as e:
        print(e)



                    
     


# MAIN STARTS
async def main():

    # Load configuration file
    configParser = ConfigParser() 
    configParser.read('config.ini')

    provisioning_host = configParser['IoTCentral']['Host']
    id_scope = configParser['IoTCentral']['IDScope']
    registration_id = configParser['IoTCentral']['DeviceId']
    symmetric_key = configParser['IoTCentral']['PrimaryKey']
    mac = configParser['macs']['1']


    registration_result = await provision_device(
                provisioning_host, id_scope, registration_id, symmetric_key
    )

    print("The complete registration result is")
    print(registration_result.registration_state)

    if registration_result.status == "assigned":
            print("Device was assigned")
            print(registration_result.registration_state.assigned_hub)
            print(registration_result.registration_state.device_id)

            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=symmetric_key,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id,
            )
    else:
        raise RuntimeError(
            "Could not provision device. Aborting Plug and Play device connection."
        )

    # Connect the client.
    await device_client.connect()

    # data_from_vetrug = getVegtrugData();

    miFloraData = MiFloraData(mac)

    # Build the message with miFloraData telemetry values.
    message = miFloraData.scan()
    
    # Send the message.
    print(message)
    
    # Send telemetry
    await send_telemetry(device_client, message)

    # Close
    await device_client.disconnect()




# EXECUTE MAIN
if __name__ == "__main__":
    asyncio.run(main())