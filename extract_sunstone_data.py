# extract_sunstone_data.py
# Extract smart_meter_data from SQL dump to CSV

import csv
import os

print("="*70)
print("SUNSTONE HOTEL DATA EXTRACTION")
print("="*70)

# Make sure SQL file is placed inside hotel_nilm folder
SQL_DUMP_PATH = "dump-mydb.sql"
OUTPUT_CSV = "data/sunstone_raw.csv"

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

def extract_to_csv():
    """Extract smart_meter_data from SQL dump to CSV"""

    print(f"\nInput:  {SQL_DUMP_PATH}")
    print(f"Output: {OUTPUT_CSV}")
    print("\nExtracting smart_meter_data...")

    in_data_section = False
    records_written = 0

    with open(SQL_DUMP_PATH, 'rb') as infile, \
         open(OUTPUT_CSV, 'w', newline='') as outfile:

        writer = csv.writer(outfile)

        # Updated CSV header (added phase)
        writer.writerow([
            'timestamp',
            'deviceId',
            'phase',
            'voltage',
            'current',
            'power',
            'pf',
            'frequency',
            'energy'
        ])

        for line_num, line in enumerate(infile, 1):
            try:
                line_str = line.decode('utf-8', errors='ignore').strip()
            except:
                continue

            # Find smart_meter_data section
            if 'COPY public.smart_meter_data' in line_str:
                in_data_section = True
                print(f"✅ Found data at line {line_num}")
                continue

            # End of section
            if in_data_section and line_str == '\\.':
                break

            # Extract data rows
            if in_data_section and line_str and not line_str.startswith('\\'):

                parts = line_str.split('\t')

                # Expected columns:
                # id, deviceId, phase, voltage, current, power,
                # energy, frequency, pf, createdAt, accountId

                if len(parts) >= 10:
                    try:
                        row = [
                            parts[9],   # timestamp (createdAt)
                            parts[1],   # deviceId
                            parts[2],   # phase (IMPORTANT)
                            parts[3],   # voltage
                            parts[4],   # current
                            parts[5],   # power
                            parts[8],   # pf
                            parts[7],   # frequency
                            parts[6],   # energy
                        ]

                        writer.writerow(row)
                        records_written += 1

                        if records_written % 10000 == 0:
                            print(f"Extracted {records_written:,} records...", end='\r')

                    except:
                        continue

    print(f"\n✅ Extracted {records_written:,} records to CSV")
    print(f"\n📁 File saved: {OUTPUT_CSV}")

    print("\n" + "-"*70)
    print("SAMPLE DATA (first 3 rows):")
    print("-"*70)

    with open(OUTPUT_CSV, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                print(" | ".join(row))
                print("-"*70)
            elif i <= 3:
                print(" | ".join(row))
            else:
                break

    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print("\n✅ Next step: Run load_hardware_to_influx.py\n")

    return records_written


if __name__ == "__main__":
    try:
        count = extract_to_csv()
        if count == 0:
            print("\n❌ No data extracted - check SQL dump path")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure SQL dump exists at:")
        print(f"  {SQL_DUMP_PATH}")
