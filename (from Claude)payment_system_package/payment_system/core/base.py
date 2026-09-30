"""Base class: the single interface shared by every payment method."""


class Payment:
    """Common interface. Subclasses override pay().

    pay() returns a message string and sets self.last_success so callers
    (receipts, QR codes, tables) know whether the payment went through.
    """

    def __init__(self, payer):
        self.payer = payer
        self.last_success = False

    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement pay()")

    def describe(self):
        return f"{self.__class__.__name__} ({self.payer})"
