
import csv
from collections import Counter

file_path = "data/raw/support_tickets.csv"

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    tickets = list(reader)

print("NEXUSAI - DATA QUALITY REPORT")
print("-" * 40)

# Check total records
print("Total tickets:", len(tickets))

# Check duplicate ticket IDs
ticket_ids = [ticket["ticket_id"] for ticket in tickets]
duplicates = len(ticket_ids) - len(set(ticket_ids))

print("Duplicate IDs:", duplicates)

# Check missing values
missing = 0

for ticket in tickets:
    for value in ticket.values():
        if not value or not value.strip():
            missing += 1

print("Missing values:", missing)

# Check category distribution
print("\nCategory Distribution:")
for category, count in Counter(
    ticket["category"] for ticket in tickets
).items():
    print(category, ":", count)

# Check priority distribution
print("\nPriority Distribution:")
for priority, count in Counter(
    ticket["priority"] for ticket in tickets
).items():
    print(priority, ":", count)

print("\nData quality check completed!")

