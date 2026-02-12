import asyncio
import random
import logging
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext




SLAVE_ID = 1          # ID 
ADDRESS_PV = 0        # Register0: PV (W)
ADDRESS_BATTERY = 1   # Register1: % Battery
PORT = 5020           # PORT to connect
async def simulation_task(context):
    
    print("Start simulation data")
    
    #ID = 1
    slave_context = context[SLAVE_ID]
    
    battery_level = 50 # Battery starting from 50%
    
    while True:
        # 1. Simulate PV (from 3000W to 5000W)
        pv_power = random.randint(3000, 5000)
        
        # 2. Simulate the change of Battery 
        change = random.choice([-1, 0, 1, 2])
        battery_level += change
        
        # Check Battery
        if battery_level > 100: battery_level = 100
        if battery_level < 0: battery_level = 0
        
        # 3. Update register (Holding Register FC:3)
        slave_context.setValues(3, ADDRESS_PV, [pv_power])
        slave_context.setValues(3, ADDRESS_BATTERY, [battery_level])
        
        print(f"[Smart Logger] update   : PV={pv_power}W | Pin={battery_level}%")
        
        # sleep 3s before continue to update
        await asyncio.sleep(3)

async def run_server():
    #Create the memory for Smart Logger 
    store = ModbusDeviceContext(
        hr=ModbusSequentialDataBlock(0, [0]*10), # Holding Registers
    )
    context = ModbusServerContext(devices={1: store}, single=False)
    

    asyncio.create_task(simulation_task(context))
    
    print(f"Server is running at: {PORT}")

    await StartAsyncTcpServer(context, address=("0.0.0.0", PORT))

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Stop Server.")