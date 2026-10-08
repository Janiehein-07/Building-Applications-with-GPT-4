from datetime import datetime


def save_reply(customer_email, reply, intent):

    with open(
        "outputs/generated_reply.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n" + "=" * 60 + "\n")
        file.write("INTELLIGENT EMAIL ASSISTANT\n")
        file.write("=" * 60 + "\n")

        file.write(f"Date: {datetime.now()}\n")
        file.write(f"Intent: {intent}\n")

        file.write("\nCustomer Email:\n")
        file.write(customer_email)

        file.write("\n\nGenerated Reply:\n")
        file.write(reply)

        file.write("\n" + "=" * 60 + "\n")

    print("\nReply saved successfully!")