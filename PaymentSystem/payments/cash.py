from .payment import Payment

class CashPayment(Payment):

    def pay(self, amount):
        return f"Paid ₱{amount:.2f} using Cash."
