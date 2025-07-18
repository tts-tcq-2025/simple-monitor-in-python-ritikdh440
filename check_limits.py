# Constants for breach types
NORMAL = 'NORMAL'
LOW_BREACH = 'LOW'
HIGH_BREACH = 'HIGH'

# Thresholds for each vital
VITAL_LIMITS = {
    'temperature': {'min': 0, 'max': 45},
    'soc': {'min': 20, 'max': 80},
    'charge_rate': {'min': 0, 'max': 0.8}
}

# Function to infer breach type
def infer_breach(value, min_limit, max_limit):
    if value < min_limit:
        return LOW_BREACH
    if value > max_limit:
        return HIGH_BREACH
    return NORMAL

# Function to check a single vital
def check_vital(vital_name, value):
    limits = VITAL_LIMITS[vital_name]
    breach = infer_breach(value, limits['min'], limits['max'])
    return {
        'vital': vital_name,
        'value': value,
        'breach': breach
    }

# Function to handle all reporting
def report_abnormal_vitals(vitals, reporter):
    for vital in vitals:
        reporter(f"{vital['vital'].capitalize()} is {vital['breach']}! Value: {vital['value']}")

# Main function
def battery_is_ok(temperature, soc, charge_rate, reporter=print):
    results = [
        check_vital('temperature', temperature),
        check_vital('soc', soc),
        check_vital('charge_rate', charge_rate)
    ]
    abnormal_vitals = [res for res in results if res['breach'] != NORMAL]
    
    report_abnormal_vitals(abnormal_vitals, reporter)
    return len(abnormal_vitals) == 0


# Basic inline test
if __name__ == '__main__':
    assert battery_is_ok(25, 70, 0.7) is True
    assert battery_is_ok(50, 85, 0) is False
