from pymodbus.client.sync import ModbusTcpClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer


def check_adapter_availability(host: str, port: str or int):
    client = ModbusTcpClient(
        host=host,
        port=port,
        stopbits=1,
        baudrate=9600,
        bytesize=8,
        retries=3,
        timeout=0.5,
        framer=ModbusRtuFramer
    )
    connection = client.connect()
    client.close()
    return connection
