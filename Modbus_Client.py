import asyncio
from pymodbus.client import AsyncModbusTcpClient


SERVER_IP = "172.20.10.2"  # IP server
SERVER_PORT = 5020          # PORT Server

async def run_monitoring():
    print(f"--- Connecting to Smart Logger at {SERVER_IP}:{SERVER_PORT} ---")
    
    client = AsyncModbusTcpClient(SERVER_IP, port=SERVER_PORT)
    await client.connect()
    
    if not client.connected:
        print("Error!")
        return

    print(">>> Connected! Start reading data...")
    
    try:
        while True:
            # Read the register0 and 1
            response = await client.read_holding_registers(address=0, count=2, device_id=1)
            
            if not response.isError():
                pv_value = response.registers[0]
                bat_value = response.registers[1]
                
                print(f"📊 [Data Real-time] Solar: {pv_value} W | Battery: {bat_value} %")
            else:
                print("Error from device.")
            
            # waitting 3s and read again (Polling)
            await asyncio.sleep(3)
            
    except KeyboardInterrupt:
        print("Stop.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Stop connect.")

if __name__ == "__main__":
    asyncio.run(run_monitoring())