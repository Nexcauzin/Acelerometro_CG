import smbus  # import SMBus module of I2C
from time import sleep  # import
import math

# Variáveis para a conexão I2C
bus = smbus.SMBus(2)  # Número do I2C utilizado
Device_Address = 0x68  # Endereço do acelerômetro no I2C

# Variáveis de correção
Fator_x = 0.0
Fator_y = 0.0
Fator_z = 0.0

# Registradores do acelerômetro (vindos do Datasheet)
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


def MPU_Init():
    # Escrever no registro de taxa de amostragem
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Escrever no registro de gerenciamento de energia
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Escrever no registro de configuração
    bus.write_byte_data(Device_Address, CONFIG, 0)

    # Escrever no registro de configuração do giroscópio
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    # Escrever no registro de habilitação de interrupção
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def read_raw_data(addr):
    # Isso porque acelerômetro e giroscópio têm 16 bit, divide em parte baixa (8 bits menos significativos) e parte alta (8 bits mais significativos)
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    # Concatenar maior e menor valor
    value = ((high << 8) | low)

    # Para obter o valor assinado do MPU6050
    if (value > 32768):
        value = value - 65536
    return value

MPU_Init()
## Fim das configurações do sensor


while True:
    # Lendo acelerometro
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    # Lendo giroscópio
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    # Convertendo as medidas para valores físicos
    AccX = acc_x / 4096 - Fator_x
    AccY = acc_y / 4096 - Fator_y
    AccZ = acc_z / 4096 - Fator_z
    RateRoll = gyro_x / 65.5
    RatePitch = gyro_y / 65.5
    RateYaw = gyro_z / 65.5

    # Calculando as taxas de ângulo
    AngleRoll = math.atan(AccY/math.sqrt((AccX*AccX)+(AccZ*AccZ)))*1/(3.142/180)
    AnglePitch = math.atan(AccX/math.sqrt((AccY*AccY)+(AccZ*AccZ)))*1/(3.142/180)

    # Esse print é para a calibração dos sensores
    # Basicamente o valor mostrado precisa ser = 1.00 para a posição do sensor nos eixos, serve para
    # Pegar um fator de correção para o cálculo dos ângulos
    # Comenta quando não usar
    print(f'AccX [g] = {AccX} | AccY [g] = {AccY} | AccZ = {AccZ}')

    # Printando na tela os valores de ângulo atual
    print(f'Roll angle [º] = {AngleRoll} | Pitch angle [º] = {AnglePitch}')

    sleep(1) # Delay do código, por padrão estamos usando 0.1 na telemetria