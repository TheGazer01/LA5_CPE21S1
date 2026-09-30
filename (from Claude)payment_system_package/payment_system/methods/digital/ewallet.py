from payment_system.core.base import Payment


class EWalletPayment(Payment):
    def __init__(self, payer, provider, balance):
        super().__init__(payer)
        self.provider = provider
        self.balance = balance

    def pay(self, amount):
        if self.balance < amount:
            self.last_success = False
            return (f"{self.payer}: {self.provider} payment failed. "
                    f"Balance is PHP {self.balance:.2f}.")
        self.last_success = True
        self.balance -= amount
        return (f"{self.payer}: Paid PHP {amount:.2f} via {self.provider}. "
                f"Remaining balance: PHP {self.balance:.2f}")
