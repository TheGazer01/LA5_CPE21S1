from payment_system.core.base import Payment


class BankTransferPayment(Payment):
    def __init__(self, payer, bank, reference_no):
        super().__init__(payer)
        self.bank = bank
        self.reference_no = reference_no

    def pay(self, amount):
        self.last_success = True
        return (f"{self.payer}: Transferred PHP {amount:.2f} via {self.bank}. "
                f"Reference No: {self.reference_no}")
