from payment_system.core.base import Payment


class CashPayment(Payment):
    def __init__(self, payer, cash_tendered):
        super().__init__(payer)
        self.cash_tendered = cash_tendered

    def pay(self, amount):
        if self.cash_tendered < amount:
            self.last_success = False
            return f"{self.payer}: Cash payment failed. Insufficient cash."
        self.last_success = True
        change = self.cash_tendered - amount
        return f"{self.payer}: Paid PHP {amount:.2f} in cash. Change: PHP {change:.2f}"
