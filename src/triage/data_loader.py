
import csv

def load_tickets(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        tickets = list(reader)

    return tickets


if __name__ == "__main__":
    tickets = load_tickets("data/raw/support_tickets.csv")

    print("NEXUSAI DATA LOADER")
    print("-" * 30)
    print("Total tickets loaded:", len(tickets))
    print("First ticket:", tickets[0]["text"])
