from .payment import Payment


class GCashPayment(Payment):

    def pay(self, amount):
        return f"Paid ₱{amount:.2f} using GCash."
