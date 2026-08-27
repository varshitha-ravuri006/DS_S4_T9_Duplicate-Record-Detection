"""
One-time script to generate sample_data.csv and ground_truth.csv.
Run: python scripts/generate_dataset.py
"""

import random
import csv
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Base entities — each tuple is (name, email_local, phone, address, city, pincode)
# Records in the same group are true duplicates with variations applied later.
DUPLICATE_GROUPS = [
    [
        ("Ravi Kumar", "ravi.kumar", "9876543210", "12 MG Road", "Hyderabad", "500001"),
        ("RAVI KUMAR", "ravikumar", "9876543210", "12, M.G. Road", "HYD", "500001"),
        ("Ravi K", "ravi.kumar", "9876543210", "12 MG Rd Hyderabad", "Hyderabad", "500001"),
    ],
    [
        ("Priya Sharma", "priya.sharma", "9123456780", "45 Park Street", "Kolkata", "700016"),
        ("PRIYA SHARMA", "priya_sharma", "9123456780", "45, Park St", "Kolkata", "700016"),
        ("Priya S", "priya.sharma", "9123456780", "45 Park Street Kolkata", "KOL", "700016"),
    ],
    [
        ("Amit Patel", "amit.patel", "9988776655", "78 Ring Road", "Ahmedabad", "380001"),
        ("Amit P", "amitpatel", "9988776655", "78 Ring Rd", "Ahmedabad", "380001"),
    ],
    [
        ("Sneha Reddy", "sneha.reddy", "9012345678", "23 Banjara Hills", "Hyderabad", "500034"),
        ("Sneha R", "sneha.reddy", "9012345678", "23 Banjara Hills Rd", "Hyderabad", "500034"),
        ("sneha reddy", "sneha_reddy", "9012345678", "23 Banjara Hills", "HYD", "500034"),
    ],
    [
        ("Rajesh Singh", "rajesh.singh", "9871234560", "56 Civil Lines", "Delhi", "110001"),
        ("RAJESH SINGH", "rajeshsingh", "9871234560", "56, Civil Lines", "New Delhi", "110001"),
    ],
    [
        ("Ananya Iyer", "ananya.iyer", "8765432109", "89 Residency Road", "Bangalore", "560025"),
        ("Ananya I", "ananya.iyer", "8765432109", "89 Residency Rd", "Bengaluru", "560025"),
        ("Ananya Iyer", "ananya_iyer", "8765432109", "89 Residency Road Bangalore", "Bangalore", "560025"),
    ],
    [
        ("Vikram Mehta", "vikram.mehta", "9654321098", "34 Linking Road", "Mumbai", "400050"),
        ("Vikram M", "vikrammehta", "9654321098", "34 Linking Rd", "Mumbai", "400050"),
    ],
    [
        ("Kavita Nair", "kavita.nair", "9543210987", "67 Marine Drive", "Mumbai", "400002"),
        ("KAVITA NAIR", "kavita.nair", "9543210987", "67 Marine Dr", "Mumbai", "400002"),
        ("Kavita N", "kavita_nair", "9543210987", "67 Marine Drive Mumbai", "MUM", "400002"),
    ],
    [
        ("Deepak Gupta", "deepak.gupta", "9432109876", "90 Connaught Place", "Delhi", "110001"),
        ("Deepak G", "deepakgupta", "9432109876", "90 CP", "Delhi", "110001"),
    ],
    [
        ("Meera Joshi", "meera.joshi", "9321098765", "11 FC Road", "Pune", "411004"),
        ("Meera J", "meera.joshi", "9321098765", "11 Fergusson College Road", "Pune", "411004"),
        ("MEERA JOSHI", "meera_joshi", "9321098765", "11 FC Rd Pune", "Pune", "411004"),
    ],
    [
        ("Arjun Desai", "arjun.desai", "9210987654", "22 CG Road", "Ahmedabad", "380009"),
        ("Arjun D", "arjundesai", "9210987654", "22 CG Rd", "Ahmedabad", "380009"),
    ],
    [
        ("Lakshmi Rao", "lakshmi.rao", "9109876543", "33 Jubilee Hills", "Hyderabad", "500033"),
        ("Lakshmi R", "lakshmi.rao", "9109876543", "33 Jubilee Hills Rd", "Hyderabad", "500033"),
    ],
    [
        ("Suresh Babu", "suresh.babu", "9098765432", "44 Anna Salai", "Chennai", "600002"),
        ("Suresh B", "sureshbabu", "9098765432", "44 Anna Salai Chennai", "Chennai", "600002"),
        ("SURESH BABU", "suresh_babu", "9098765432", "44 Anna Salai", "CHN", "600002"),
    ],
    [
        ("Divya Krishnan", "divya.krishnan", "8987654321", "55 MG Road", "Bangalore", "560001"),
        ("Divya K", "divya.krishnan", "8987654321", "55 MG Rd", "Bengaluru", "560001"),
    ],
    [
        ("Manoj Tiwari", "manoj.tiwari", "8876543210", "66 Hazratganj", "Lucknow", "226001"),
        ("Manoj T", "manojtiwari", "8876543210", "66 Hazrat Ganj", "Lucknow", "226001"),
        ("MANOJ TIWARI", "manoj_tiwari", "8876543210", "66 Hazratganj Lucknow", "Lucknow", "226001"),
    ],
    [
        ("Pooja Verma", "pooja.verma", "8765432190", "77 Mall Road", "Dehradun", "248001"),
        ("Pooja V", "pooja.verma", "8765432190", "77 Mall Rd", "Dehradun", "248001"),
    ],
    [
        ("Rahul Khanna", "rahul.khanna", "8654321090", "88 Sector 17", "Chandigarh", "160017"),
        ("Rahul K", "rahulkhanna", "8654321090", "88 Sec 17", "Chandigarh", "160017"),
    ],
    [
        ("Neha Agarwal", "neha.agarwal", "8543210980", "99 Park Avenue", "Jaipur", "302001"),
        ("Neha A", "neha.agarwal", "8543210980", "99 Park Ave", "Jaipur", "302001"),
        ("NEHA AGARWAL", "neha_agarwal", "8543210980", "99 Park Avenue Jaipur", "Jaipur", "302001"),
    ],
    [
        ("Karan Malhotra", "karan.malhotra", "8432109870", "101 Brigade Road", "Bangalore", "560001"),
        ("Karan M", "karanmalhotra", "8432109870", "101 Brigade Rd", "Bengaluru", "560001"),
    ],
    [
        ("Swati Pillai", "swati.pillai", "8321098760", "202 MG Road", "Kochi", "682016"),
        ("Swati P", "swati.pillai", "8321098760", "202 MG Rd Kochi", "Kochi", "682016"),
    ],
    [
        ("Nikhil Bose", "nikhil.bose", "8210987650", "303 Park Street", "Kolkata", "700016"),
        ("Nikhil B", "nikhilbose", "8210987650", "303 Park St", "Kolkata", "700016"),
    ],
    [
        ("Tanvi Shah", "tanvi.shah", "8109876540", "404 Ashram Road", "Ahmedabad", "380009"),
        ("Tanvi S", "tanvi.shah", "8109876540", "404 Ashram Rd", "Ahmedabad", "380009"),
        ("TANVI SHAH", "tanvi_shah", "8109876540", "404 Ashram Road Ahmedabad", "Ahmedabad", "380009"),
    ],
    [
        ("Gaurav Chopra", "gaurav.chopra", "8098765430", "505 Rajpath", "Delhi", "110001"),
        ("Gaurav C", "gauravchopra", "8098765430", "505 Raj Path", "New Delhi", "110001"),
    ],
    [
        ("Isha Menon", "isha.menon", "7987654320", "606 Marine Drive", "Mumbai", "400002"),
        ("Isha M", "isha.menon", "7987654320", "606 Marine Dr", "Mumbai", "400002"),
    ],
    [
        ("Harsh Vardhan", "harsh.vardhan", "7876543210", "707 MI Road", "Jaipur", "302001"),
        ("Harsh V", "harshvardhan", "7876543210", "707 Mirza Ismail Road", "Jaipur", "302001"),
        ("HARSH VARDHAN", "harsh_vardhan", "7876543210", "707 MI Rd Jaipur", "Jaipur", "302001"),
    ],
    [
        ("Ritu Saxena", "ritu.saxena", "7765432100", "808 Cantonment", "Pune", "411001"),
        ("Ritu S", "ritu.saxena", "7765432100", "808 Cantonment Area", "Pune", "411001"),
    ],
    [
        ("Aditya Roy", "aditya.roy", "7654321090", "909 Salt Lake", "Kolkata", "700064"),
        ("Aditya R", "adityaroy", "7654321090", "909 Salt Lake City", "Kolkata", "700064"),
    ],
    [
        ("Shreya Das", "shreya.das", "7543210980", "111 Indiranagar", "Bangalore", "560038"),
        ("Shreya D", "shreyadas", "7543210980", "111 Indira Nagar", "Bengaluru", "560038"),
        ("SHREYA DAS", "shreya.das", "7543210980", "111 Indiranagar Bangalore", "Bangalore", "560038"),
    ],
    [
        ("Varun Sethi", "varun.sethi", "7432109870", "222 Sector 62", "Noida", "201301"),
        ("Varun S", "varun.sethi", "7432109870", "222 Sec 62", "Noida", "201301"),
    ],
    [
        ("Anjali Kulkarni", "anjali.kulkarni", "7321098760", "333 FC Road", "Pune", "411004"),
        ("Anjali K", "anjalikulkarni", "7321098760", "333 Fergusson College Rd", "Pune", "411004"),
    ],
    [
        ("Rohit Bansal", "rohit.bansal", "7210987650", "444 Mall Road", "Amritsar", "143001"),
        ("Rohit B", "rohit.bansal", "7210987650", "444 Mall Rd", "Amritsar", "143001"),
        ("ROHIT BANSAL", "rohit_bansal", "7210987650", "444 Mall Road Amritsar", "Amritsar", "143001"),
    ],
    [
        ("Kritika Jain", "kritika.jain", "7109876540", "555 C Scheme", "Jaipur", "302001"),
        ("Kritika J", "kritikajain", "7109876540", "555 C-Scheme", "Jaipur", "302001"),
    ],
    [
        ("Sanjay Mishra", "sanjay.mishra", "7098765430", "666 Gomti Nagar", "Lucknow", "226010"),
        ("Sanjay M", "sanjay.mishra", "7098765430", "666 Gomti Nagar Ext", "Lucknow", "226010"),
    ],
    [
        ("Preeti Chawla", "preeti.chawla", "6987654320", "777 Model Town", "Delhi", "110009"),
        ("Preeti C", "preetichawla", "6987654320", "777 Model Town Delhi", "New Delhi", "110009"),
        ("PREETI CHAWLA", "preeti_chawla", "6987654320", "777 Model Town", "Delhi", "110009"),
    ],
    [
        ("Abhishek Dutta", "abhishek.dutta", "6876543210", "888 Salt Lake Sector V", "Kolkata", "700091"),
        ("Abhishek D", "abhishek.dutta", "6876543210", "888 Sector V Salt Lake", "Kolkata", "700091"),
    ],
]

# Similar names but DIFFERENT people (for false-positive demonstration)
SIMILAR_BUT_DIFFERENT = [
    ("Ravi Kumar", "ravi.kumar2", "9111111111", "100 Hitech City", "Hyderabad", "500081"),
    ("Ravi Kumari", "ravi.kumari", "9222222222", "200 Gachibowli", "Hyderabad", "500032"),
    ("Priya Sharma", "priya.sharma2", "9333333333", "300 Salt Lake", "Kolkata", "700064"),
    ("Amit Patel", "amit.patel2", "9444444444", "400 Satellite", "Ahmedabad", "380015"),
    ("Rajesh Singh", "rajesh.singh2", "9555555555", "500 Rohini", "Delhi", "110085"),
    ("Ananya Iyer", "ananya.iyer2", "9666666666", "600 Whitefield", "Bangalore", "560066"),
    ("Vikram Mehta", "vikram.mehta2", "9777777777", "700 Andheri", "Mumbai", "400053"),
    ("Deepak Gupta", "deepak.gupta2", "9888888888", "800 Dwarka", "Delhi", "110075"),
    ("Suresh Babu", "suresh.babu2", "9999999990", "900 T Nagar", "Chennai", "600017"),
    ("Neha Agarwal", "neha.agarwal2", "9000000001", "1000 Malviya Nagar", "Jaipur", "302017"),
]

# Unique standalone records
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Ananya", "Diya", "Aadhya", "Pari", "Myra", "Sara", "Ira", "Avni", "Riya", "Navya",
    "Mohit", "Rakesh", "Sunil", "Vinod", "Pradeep", "Naveen", "Ashok", "Ramesh", "Mahesh", "Dinesh",
    "Sunita", "Geeta", "Rekha", "Sushma", "Lata", "Usha", "Asha", "Nirmala", "Kamala", "Padma",
]
LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Reddy", "Nair", "Iyer", "Patel", "Shah",
    "Mehta", "Joshi", "Rao", "Das", "Bose", "Chopra", "Malhotra", "Khanna", "Saxena", "Pillai",
]
CITIES = [
    ("Hyderabad", "500001"), ("Bangalore", "560001"), ("Mumbai", "400001"), ("Delhi", "110001"),
    ("Chennai", "600001"), ("Kolkata", "700001"), ("Pune", "411001"), ("Ahmedabad", "380001"),
    ("Jaipur", "302001"), ("Lucknow", "226001"), ("Chandigarh", "160001"), ("Kochi", "682001"),
    ("Noida", "201301"), ("Indore", "452001"), ("Bhopal", "462001"), ("Nagpur", "440001"),
]
STREETS = ["MG Road", "Park Street", "Ring Road", "Station Road", "Main Road", "Church Street", "Lake View"]

DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "rediffmail.com"]


def format_email(local: str, variant: int = 0) -> str:
    """Apply small email formatting variations."""
    domain = random.choice(DOMAINS)
    if variant == 0:
        return f"{local}@{domain}"
    if "@" in local:
        return local
    return f"{local}@{domain}"


def normalize_phone_digits(phone: str) -> str:
    """Strip formatting and keep last 10 digits."""
    digits = "".join(c for c in phone if c.isdigit())
    return digits[-10:] if len(digits) >= 10 else digits


def format_phone(phone: str, variant: int) -> str:
    """Apply phone formatting variations to a plain 10-digit number."""
    digits = normalize_phone_digits(phone)
    if variant == 0:
        return digits
    if variant == 1:
        return f"+91 {digits}"
    if variant == 2:
        return f"+91-{digits[:5]}-{digits[5:]}"
    return digits


def apply_missing(value: str, prob: float = 0.08) -> str:
    """Randomly introduce missing values."""
    if random.random() < prob:
        return ""
    return value


def generate_unique_records(count: int, start_id: int) -> list[dict]:
    """Generate genuinely unique customer records."""
    records = []
    used_phones = set()

    for i in range(count):
        record_id = start_id + i
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        city, pincode = random.choice(CITIES)
        street_num = random.randint(1, 999)
        street = random.choice(STREETS)
        address = f"{street_num} {street} {city}"

        # Ensure unique phone
        while True:
            phone = str(random.randint(6000000000, 9999999999))
            if phone not in used_phones:
                used_phones.add(phone)
                break

        email_local = f"{first.lower()}.{last.lower()}{random.randint(1, 999)}"
        email = f"{email_local}@{random.choice(DOMAINS)}"

        records.append({
            "record_id": record_id,
            "name": apply_missing(name),
            "email": apply_missing(email),
            "phone": apply_missing(phone),
            "address": apply_missing(address),
            "city": apply_missing(city),
            "pincode": apply_missing(pincode),
        })

    return records


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    ground_truth_pairs = []
    record_id = 1

    # Add duplicate groups
    for group_idx, group in enumerate(DUPLICATE_GROUPS):
        group_ids = []
        for variant_idx, (name, email_local, phone, address, city, pincode) in enumerate(group):
            email = format_email(email_local, variant_idx % 2)
            phone_fmt = format_phone(phone, variant_idx)

            rec = {
                "record_id": record_id,
                "name": apply_missing(name, 0.05),
                "email": apply_missing(email, 0.06),
                "phone": apply_missing(phone_fmt, 0.04),
                "address": apply_missing(address, 0.07),
                "city": apply_missing(city, 0.03),
                "pincode": apply_missing(pincode, 0.02),
            }
            records.append(rec)
            group_ids.append(record_id)
            record_id += 1

        # All pairs within a group are true duplicates
        for i in range(len(group_ids)):
            for j in range(i + 1, len(group_ids)):
                ground_truth_pairs.append({
                    "record_1": group_ids[i],
                    "record_2": group_ids[j],
                    "is_duplicate": 1,
                    "group_id": group_idx + 1,
                })

    # Add similar-but-different records (NOT in ground truth as duplicates)
    for name, email_local, phone, address, city, pincode in SIMILAR_BUT_DIFFERENT:
        records.append({
            "record_id": record_id,
            "name": name,
            "email": f"{email_local}@{random.choice(DOMAINS)}",
            "phone": phone,
            "address": address,
            "city": city,
            "pincode": pincode,
        })
        record_id += 1

    # Fill up to ~420 records with unique entries
    target_total = 420
    remaining = target_total - len(records)
    if remaining > 0:
        records.extend(generate_unique_records(remaining, record_id))

    # Shuffle so duplicates aren't grouped together
    random.shuffle(records)

    # Write sample_data.csv
    fieldnames = ["record_id", "name", "email", "phone", "address", "city", "pincode"]
    sample_path = DATA_DIR / "sample_data.csv"
    with open(sample_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Write ground_truth.csv
    gt_path = DATA_DIR / "ground_truth.csv"
    with open(gt_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_1", "record_2", "is_duplicate", "group_id"])
        writer.writeheader()
        writer.writerows(ground_truth_pairs)

    print(f"Created {sample_path} with {len(records)} records")
    print(f"Created {gt_path} with {len(ground_truth_pairs)} duplicate pairs")
    print(f"Duplicate groups: {len(DUPLICATE_GROUPS)}")
    print(f"Similar-but-different records: {len(SIMILAR_BUT_DIFFERENT)}")


if __name__ == "__main__":
    main()
