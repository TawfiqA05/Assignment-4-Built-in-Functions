def parse_date(date_str):
    """Extract the year and month from the date in YYYYMMDD format."""
    return date_str[:6]  # First 6 characters represent YYYYMM

def get_highest_ratio_state(file_path):
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        data = file.readlines()

    monthly_data = {}

    # Identify the column headers from the first line of the file
    headers = data[0].strip().split(',')
    date_index = headers.index('date')
    state_index = headers.index('state')
    positive_index = headers.index('positive')
    hospitalization_index = headers.index('hospitalizedCurrently')

    # Process each line after the header
    for line in data[1:]:
        columns = line.strip().split(',')

        # Extract relevant fields
        date = columns[date_index]
        state = columns[state_index]
        positive_tests = columns[positive_index]
        hospitalizations = columns[hospitalization_index]

        # Skip rows with missing or invalid data
        if not positive_tests or not hospitalizations:
            continue

        try:
            positive_tests = float(positive_tests)
            hospitalizations = float(hospitalizations)
        except ValueError:
            continue  # Skip rows with non-numeric data

        # Ensure we don't divide by zero
        if hospitalizations == 0:
            continue

        # Calculate the ratio
        ratio = positive_tests / hospitalizations
        month = parse_date(date)

        # Initialize month and state entries if not present
        if month not in monthly_data:
            monthly_data[month] = {}

        # Store the maximum ratio for each state in the month
        if state not in monthly_data[month]:
            monthly_data[month][state] = ratio
        else:
            monthly_data[month][state] = max(monthly_data[month][state], ratio)

    # Determine the state with the highest ratio for each month
    highest_ratio_states = {}
    for month, states in monthly_data.items():
        highest_state = max(states, key=states.get)
        highest_ratio_states[month] = (highest_state, states[highest_state])

    return highest_ratio_states

# Example usage with your file path
file_path = "/Users/tawfiqabulail/Downloads/Information Infrastructure I /covid_data_set.csv"
highest_ratio_states = get_highest_ratio_state(file_path)

# Display the results
for month, (state, ratio) in highest_ratio_states.items():
    print(f"Month: {month}, State: {state}, Ratio: {ratio}")
