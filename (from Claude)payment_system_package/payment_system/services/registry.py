"""Registry: maps a display name to a payment class and its input fields.

The GUI builds its form from this table, so adding a new payment type only
means adding one row here (polymorphism keeps everything else unchanged).
"""
from payment_system.methods import (
    CashPayment,
    CreditCardPayment,
    DebitCardPayment,
    EWalletPayment,
    BankTransferPayment,
)

# name -> (class, [(field label, type), ...])
METHOD_REGISTRY = {
    "Cash": (CashPayment, [("Cash tendered", float)]),
    "Credit Card": (CreditCardPayment, [("Card number", str)]),
    "Debit Card": (DebitCardPayment, [("Card number", str), ("Balance", float)]),
    "E-Wallet": (EWalletPayment, [("Provider", str), ("Balance", float)]),
    "Bank Transfer": (BankTransferPayment, [("Bank", str), ("Reference no.", str)]),
}


def build_payment(method_name, payer, raw_values):
    """Create the right Payment object from text typed into the form."""
    cls, fields = METHOD_REGISTRY[method_name]
    args = []
    for (label, typ), raw in zip(fields, raw_values):
        raw = raw.strip()
        if not raw:
            raise ValueError(f"'{label}' is required.")
        try:
            args.append(typ(raw))
        except ValueError:
            raise ValueError(f"'{label}' must be a valid {typ.__name__}.")
    return cls(payer, *args)
