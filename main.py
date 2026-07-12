import storage
import models
import order_service
import payments_service
import display

def main():
    data = storage.load_data()

    while True:
        print("\n--- Portrait Order Tracker ---")
        print("1. Create Order")
        print("2. View Dashboard")
        print("3. List All Orders")
        print("4. Update Order Status")
        print("5. Record Payment")
        print("6. Search Orders")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            client_name = input("Enter Client name: ")
            client_contact = input("Enter client contact: ")
            paper_size = input("What paper size did they choose (A3/A4)? ")
            subject_type = input("What's the subject type (single, couple, group)? ")

            framing_input = input("Include Framing? (y/n): ").lower()
            frame = framing_input == "y" or framing_input == "yes"

            rush_input = input("Is it a rush order (y/n)?: ").lower()
            rush_order = rush_input == "y" or rush_input == "yes"

            lamination_input = input("To be laminated (y/n)?: ").lower()
            lamination = lamination_input == "y" or lamination_input == "yes"

            digital_scan_input = input("To be scanned (y/n)?: ").lower()
            digital_scan = digital_scan_input == "y" or digital_scan_input == "yes"
            
            new_order = order_service.create_order(data,client_name, client_contact, paper_size, subject_type, frame, rush_order, lamination, digital_scan)
            print("Order created successfully!")

            print(display.format_order_summary(new_order))

        elif choice == "2":
            display.print_dashboard(data)

        elif choice == "3":
            display.print_order_list(data['orders'])

        elif choice == "4":
            order_id = input("Enter order ID: ").upper()
            new_status = input("Enter new status: ").upper()

            result = order_service.update_status(data, order_id, new_status)

            if result is True:
                print("Status updated successfully.")
            elif result is False:
                print("Invalid status transition.")
            else:
                print("Order not found.")

        elif choice == "5":
            record_id = input("Enter order ID: ").upper()
            amount_paid = int(input("Enter amount received: "))

            result = payments_service.record_payment(data, record_id, amount_paid)

            if result:
                print("Payment recorded.")
            else:
                print("Order not found.")

        elif choice == "6":
            status = input("Filter by status (or press Enter to skip): ").upper() or None
            client_name = input("Filter by client name (or press Enter to skip): ") or None

            matches = order_service.filter_orders(data, status, client_name)
            display.print_order_list(matches)

        elif choice == "7":
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()