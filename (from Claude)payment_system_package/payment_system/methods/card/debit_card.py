from payment_system.core.base import Payment


class DebitCardPayment(Payment):
    def __init__(self, payer, card_number, balance):
        super().__init__(payer)
        self.card_number = card_number
        self.balance = balance

    def pay(self, amount):
        masked = "**** **** **** " + self.card_number[-4:]
        if self.balance < amount:
            self.last_success = False
            return f"{self.payer}: Debit card {masked} declined. Insufficient funds."
        self.last_success = True
        self.balance -= amount
        return (f"{self.payer}: Paid PHP {amount:.2f} with debit card {masked}. "
                f"Remaining balance: PHP {self.balance:.2f}")
