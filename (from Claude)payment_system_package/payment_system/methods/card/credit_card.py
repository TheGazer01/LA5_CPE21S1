from payment_system.core.base import Payment


class CreditCardPayment(Payment):
    FEE_RATE = 0.02  # 2% processing fee

    def __init__(self, payer, card_number):
        super().__init__(payer)
        self.card_number = card_number

    def pay(self, amount):
        self.last_success = True
        fee = amount * self.FEE_RATE
        total = amount + fee
        masked = "**** **** **** " + self.card_number[-4:]
        return (f"{self.payer}: Charged PHP {total:.2f} to credit card {masked} "
                f"(includes PHP {fee:.2f} fee).")
