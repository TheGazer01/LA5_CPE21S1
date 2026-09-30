from .payment import Payment


class BankTransferPayment(Payment):

    def pay(self, amount):
        return f"Paid ₱{amount:.2f} using Bank Transfer."
