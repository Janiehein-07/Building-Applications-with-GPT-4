def get_customer_input():
    print("\n========== CUSTOMER EMAIL ==========")

    name = input("Customer Name: ")
    subject = input("Email Subject: ")
    email = input("Customer Email: ")

    print("\n========== ENTERED DETAILS ==========")
    print("Customer Name :", name)
    print("Subject       :", subject)
    print("Customer Email:", email)

    return {
        "name": name,
        "subject": subject,
        "email": email
    }