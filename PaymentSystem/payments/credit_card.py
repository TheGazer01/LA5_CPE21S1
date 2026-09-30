from .payment import Payment


class CreditCardPayment(Payment):

    def pay(self, amount):
        return f"Paid ₱{amount:.2f} using Credit Card."
