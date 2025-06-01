import operator

# Constants
DELIMITER = '|'
DATE_FORMAT = "%Y/%m/%d"

# Load and parse the dataset
def load_dataset(filename):
    try:
        with open(filename, 'r') as file:
            records = []
            for line in file:
                parts = line.strip().split(DELIMITER)
                if len(parts) != 3:
                    continue
                plate_date_time, spot_id, fee = parts
                segments = plate_date_time.split('/')
                if len(segments) != 6:
                    continue
                plate = segments[0]
                date = f"{segments[1]}/{segments[2]}/{segments[3]}"
                checkin = int(segments[4])
                checkout = int(segments[5])
                fee = int(fee)
                records.append({
                    'plate': plate,
                    'date': date,
                    'checkin': checkin,
                    'checkout': checkout,
                    'spot_id': spot_id,
                    'fee': fee
                })
            return records
    except FileNotFoundError:
        print("Error: File not found.")
        return []

# Calculate duration in minutes
def calculate_duration_minutes(checkin, checkout):
    in_minutes = (checkin // 100) * 60 + (checkin % 100)
    out_minutes = (checkout // 100) * 60 + (checkout % 100)
    return out_minutes - in_minutes

# Convert minutes to hours and minutes
def convert_to_hours_minutes(total_minutes):
    return divmod(total_minutes, 60)

# Show all records
def licence_plate_history(data):
    # Extract and show all unique license plates
    unique_plates = sorted(set(record['plate'] for record in data))
    print("Available license plates:", ", ".join(unique_plates))
    plate_input = input(">> Enter licence plate (press Enter to show all): ").strip().upper()

    if plate_input:
        filtered_data = [record for record in data if record['plate'] == plate_input]
        if not filtered_data:
            print("** No records found for this number plate.")
            return
    else:
        filtered_data = data

    # Print table header
    print("\n{:<15} {:<12} {:<16} {:<17} {:<10} {:<6}".format(
        "Licence Plate", "Date", "Check-In Time", "Check-Out Time", "Spot ID", "Fee"
    ))
    print("-" * 80)

    # Print each record in table row format
    for record in filtered_data:
        print("{:<15} {:<12} {:<16} {:<17} {:<10} ${:<5}".format(
            record['plate'],
            record['date'],
            f"{record['checkin'] // 100:02d}:{record['checkin'] % 100:02d}",
            f"{record['checkout'] // 100:02d}:{record['checkout'] % 100:02d}",
            record['spot_id'],
            record['fee']
        ))


# Summary: Total records
def peak_hour_analysis(data):
     # Count the frequency of each check-in hour
    hour_counts = {}
    for record in data:
        hour = record['checkin'] // 100  # Extract hour from HHMM
        hour_counts[hour] = hour_counts.get(hour, 0) + 1

    # Convert to list of tuples and sort by count descending
    sorted_hours = sorted(hour_counts.items(), key=operator.itemgetter(1), reverse=True)

    # Display in table format
    print("\n{:<25}{}".format("Check-In Hour", "Count"))
    print("-" * 40)
    for hour, count in sorted_hours:
        print(f"{hour:<25}{count}")

# Summary: Total revenue
def daily_revenue(data):
    # Extract all unique dates and sort them
    unique_dates = sorted(set(record['date'] for record in data))

    # Display all dates as a numbered list
    print("\nDates:")
    print("-------")
    for idx, date in enumerate(unique_dates, 1):
        print(f"{idx}. {date}")

    # Prompt user to select a date by number
    try:
        selection = int(input(">> Select a date by number: ").strip())
        if 1 <= selection <= len(unique_dates):
            selected_date = unique_dates[selection - 1]
            total = sum(record['fee'] for record in data if record['date'] == selected_date)
            print(f"\nTotal revenue for {selected_date}: ${total}")
        else:
            print("** Invalid selection.")
    except ValueError:
        print("** Invalid input.")

# Sort by fee
def avg_stay_duration(data, descending=True):
    # Sort data by fee if requested
    sorted_data = sorted(data, key=operator.itemgetter('fee'), reverse=descending)

    total_minutes = sum(calculate_duration_minutes(record['checkin'], record['checkout']) for record in sorted_data)
    average_minutes = total_minutes // len(sorted_data) if sorted_data else 0
    hrs, mins = convert_to_hours_minutes(average_minutes)

    # Print average duration
    print(f"\nAverage parking duration: {hrs} hours and {mins} minutes")


# Get average parking duration
def average_parking_duration(data):
    if not data:
        print("No data to compute.")
        return
    total_minutes = sum(calculate_duration_minutes(r['checkin'], r['checkout']) for r in data)
    avg_minutes = total_minutes // len(data)
    hrs, mins = convert_to_hours_minutes(avg_minutes)
    print(f"Average parking duration: {hrs} hours and {mins} minutes")

# Menu system
def display_menu():
    print("\n==== Parking Records Analysis Menu ====")
    print("1. Licence Plate History")
    print("2. Peak Hour Analysis")
    print("3. Daily Revenue")
    print("4. Average Stay Duration")
    print("5. Exit")

def main():
    filename = input("Enter dataset filename (e.g., data.txt): ")
    dataset = load_dataset(filename)

    if not dataset:
        return
    print(f"\nLoaded {len(dataset)} records from {filename}.\n")
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == '1':
            licence_plate_history(dataset)
        elif choice == '2':
            peak_hour_analysis(dataset)
        elif choice == '3':
            daily_revenue(dataset)
        elif choice == '4':
            avg_stay_duration(dataset)
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please choose again.")

if __name__ == "__main__":
    main()
