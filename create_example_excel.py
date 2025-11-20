"""
Create example Excel document with semiconductor component data
"""
import pandas as pd
from pathlib import Path

# Create sample semiconductor component data
data = {
    'Component_ID': [
        'SC-001', 'SC-002', 'SC-003', 'SC-004', 'SC-005',
        'SC-006', 'SC-007', 'SC-008', 'SC-009', 'SC-010'
    ],
    'Component_Name': [
        'MOSFET Power Transistor',
        'Voltage Regulator IC',
        'Crystal Oscillator',
        'Schottky Diode',
        'LED Driver IC',
        'Operational Amplifier',
        'Microcontroller',
        'Flash Memory Chip',
        'Temperature Sensor',
        'Analog-to-Digital Converter'
    ],
    'Category': [
        'Transistor',
        'Integrated Circuit',
        'Oscillator',
        'Diode',
        'Integrated Circuit',
        'Amplifier',
        'Microcontroller',
        'Memory',
        'Sensor',
        'Converter'
    ],
    'Manufacturer': [
        'Infineon',
        'Texas Instruments',
        'NDK',
        'Vishay',
        'Analog Devices',
        'STMicroelectronics',
        'Microchip',
        'Samsung',
        'Maxim Integrated',
        'Analog Devices'
    ],
    'Part_Number': [
        'IRF540N',
        'LM7805',
        'NX3225SA',
        'MBR1545CT',
        'LT3484',
        'LM358',
        'PIC18F4550',
        'K9F1G08U0E',
        'DS18B20',
        'AD7091R'
    ],
    'Voltage_Rating_V': [
        '100V', '5V', '3.3V', '45V', '40V',
        '36V', '5V', '3.3V', '5V', '2.5V'
    ],
    'Current_Rating_A': [
        '33A', '1A', 'N/A', '15A', '2A',
        'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    ],
    'Package_Type': [
        'TO-220', 'TO-220', 'SMD', 'TO-220', 'SMD',
        'DIP-8', 'DIP-40', 'TSOP', 'TO-92', 'SOT-23'
    ],
    'Operating_Temperature_C': [
        '-55 to 175', '-40 to 125', '-40 to 85', '-65 to 175', '-40 to 125',
        '0 to 70', '-40 to 85', '-25 to 85', '-55 to 125', '-40 to 125'
    ],
    'Description': [
        'N-channel power MOSFET with low on-resistance',
        'Positive voltage regulator with fixed 5V output',
        '32.768 kHz crystal oscillator in small package',
        'Schottky barrier rectifier with low forward voltage',
        'Step-down LED driver with dimming capability',
        'Dual operational amplifier with low power consumption',
        '8-bit microcontroller with USB support',
        '1Gb NAND flash memory with parallel interface',
        'Digital temperature sensor with 1-wire interface',
        '12-bit ADC with SPI interface and low power'
    ],
    'Application': [
        'Power switching, motor control',
        'Voltage regulation, power supply',
        'Clock generation, timing circuits',
        'Power rectification, fast switching',
        'LED lighting, display backlight',
        'Signal conditioning, filtering',
        'Embedded systems, automation',
        'Data storage, firmware',
        'Temperature monitoring, HVAC',
        'Data acquisition, measurement'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_dir = Path("examples")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "semiconductor_components.xlsx"
df.to_excel(output_file, index=False, sheet_name='Components')

print(f"Example Excel file created: {output_file}")
print(f"Total components: {len(df)}")
print("\nSample data:")
print(df.head().to_string())

