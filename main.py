import operator
from datetime import datetime

# === Constants ===
DELIMITER = '|'
DATE_FORMAT = "%Y/%m/%d"
MIN_FIELDS = 6


# === Function: Load and validate dataset ===
def load_dataset(filename):
    """
    Load the dataset from a text file, parse and validate each record.
    Returns a list of dictionaries containing valid parking records.
    """
    try:
        with open(filename, 'r') as file:
            records = []
            line_number = 0
            for line in file:
                line_number += 1
                try:
                    parts = line.strip().split(DELIMITER)
                    if len(parts) != MIN_FIELDS:
                        print(f"Skipping line {line_number}: expected {MIN_FIELDS} fields, got {len(parts)}")
                        continue

                    plate = parts[0].strip().upper()
                    date = parts[1].strip()
                    checkin = int(parts[2].strip())
                    checkout = int(parts[3].strip())
                    spot_id = parts[4].strip().upper()
                    fee = int(parts[5].strip())

                    # Validate date format
                    datetime.strptime(date, DATE_FORMAT)

                    # Add validated record
                    records.append({
                        'plate': plate,
                        'date': date,
                        'checkin': checkin,
                        'checkout': checkout,
                        'spot_id': spot_id,
                        'fee': fee
                    })

                except ValueError as ve:
                    print(f"Invalid data format on line {line_number}: {ve}")
                except Exception as e:
                    print(f"Error processing line {line_number}: {e}")
            return records

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Unexpected error while loading dataset: {e}")
    return []


# === Function: Calculate duration in minutes ===
def calculate_duration_minutes(checkin, checkout):
    """
    Calculate total minutes between check-in and check-out times.
    """
    try:
        in_minutes = (checkin // 100) * 60 + (checkin % 100)
        out_minutes = (checkout // 100) * 60 + (checkout % 100)
        return max(0, out_minutes - in_minutes)
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return 0


# === Function: Convert minutes to hours and minutes ===
def convert_to_hours_minutes(total_minutes):
    """
    Convert total minutes to (hours, minutes) tuple.
    """
    return divmod(total_minutes, 60)


# === Function: Show license plate history ===
def licence_plate_history(data):
    """
    Show all records for a selected license plate, or all plates if none specified.
    """
    try:
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

        print("\n{:<15} {:<12} {:<16} {:<17} {:<10} {:<6}".format(
            "Licence Plate", "Date", "Check-In Time", "Check-Out Time", "Spot ID", "Fee"
        ))
        print("-" * 80)

        for record in filtered_data:
            checkin = f"{record['checkin'] // 100:02d}:{record['checkin'] % 100:02d}"
            checkout = f"{record['checkout'] // 100:02d}:{record['checkout'] % 100:02d}"
            print("{:<15} {:<12} {:<16} {:<17} {:<10} ${:<5}".format(
                record['plate'], record['date'], checkin, checkout, record['spot_id'], record['fee']
            ))

    except Exception as e:
        print(f"Error in licence_plate_history: {e}")


# === Function: Show peak hour check-in analysis ===
def peak_hour_analysis(data):
    """
    Display check-in frequency for each hour.
    """
    try:
        hour_counts = {}
        for record in data:
            hour = record['checkin'] // 100
            hour_counts[hour] = hour_counts.get(hour, 0) + 1

        sorted_hours = sorted(hour_counts.items(), key=operator.itemgetter(1), reverse=True)

        print("\n{:<25}{}".format("Check-In Hour", "Count"))
        print("-" * 40)
        for hour, count in sorted_hours:
            print(f"{hour:02d}:00{' ' * 19}{count}")
    except Exception as e:
        print(f"Error in peak_hour_analysis: {e}")


# === Function: Calculate daily revenue ===
def daily_revenue(data):
    """
    Display total revenue collected on a user-selected date.
    """
    try:
        unique_dates = sorted(set(record['date'] for record in data))

        print("\nDates:")
        print("-------")
        for idx, date in enumerate(unique_dates, 1):
            print(f"{idx}. {date}")

        selection = input(">> Select a date by number: ").strip()
        if not selection.isdigit():
            print("** Invalid input. Enter a valid number.")
            return

        index = int(selection)
        if 1 <= index <= len(unique_dates):
            selected_date = unique_dates[index - 1]
            total = sum(record['fee'] for record in data if record['date'] == selected_date)
            print(f"\nTotal revenue for {selected_date}: ${total}")
        else:
            print("** Invalid selection.")

    except Exception as e:
        print(f"Error in daily_revenue: {e}")


# === Function: Calculate average stay duration ===
def avg_stay_duration(data):
    """
    Display average parking duration for all records.
    """
    try:
        if not data:
            print("No data available to compute average duration.")
            return

        total_minutes = sum(calculate_duration_minutes(record['checkin'], record['checkout']) for record in data)
        average_minutes = total_minutes // len(data)
        hrs, mins = convert_to_hours_minutes(average_minutes)
        print(f"\nAverage parking duration: {hrs} hours and {mins} minutes")

    except Exception as e:
        print(f"Error in avg_stay_duration: {e}")


# === Function: Display main menu ===
def display_menu():
    """
    Show the menu options.
    """
    print("\n==== Parking Records Analysis Menu ====")
    print("1. Licence Plate History")
    print("2. Peak Hour Analysis")
    print("3. Daily Revenue")
    print("4. Average Stay Duration")
    print("5. Exit")


# === Main control function ===
def main():
    """
    Entry point for the parking record analysis program.
    """
    try:
        filename = input("Enter dataset filename (e.g., data.txt): ").strip()
        dataset = load_dataset(filename)

        if not dataset:
            print("No valid records loaded. Program will exit.")
            return

        print(f"\nLoaded {len(dataset)} valid records from '{filename}'.\n")

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

    except Exception as e:
        print(f"Fatal error in main program: {e}")


# === Program Entry ===
if __name__ == "__main__":
    main()
