"""Entry point.

    python main.py          -> launches the tkinter GUI
    python main.py --cli    -> runs the console demo (rich)
"""
import sys

from payment_system import PaymentProcessor
from payment_system.methods import (
    CashPayment,
    CreditCardPayment,
    DebitCardPayment,
    EWalletPayment,
    BankTransferPayment,
)
from payment_system.services.console import console, show_banner, show_summary


def run_cli():
    show_banner()
    methods = [
        CashPayment("Juan", 1000),
        CreditCardPayment("Maria", "1234567812345678"),
        DebitCardPayment("Jose", "8765432187654321", 900),
        EWalletPayment("Pedro", "GCash", 500),
        BankTransferPayment("Ana", "BDO", "REF-20260929-001"),
    ]
    processor = PaymentProcessor(output=console.print)
    amount = 750.00
    console.print(f"\nAmount due: [bold]PHP {amount:,.2f}[/bold]\n")
    processor.process_all(methods, amount)
    console.print()
    show_summary(processor.history)


def main():
    if "--cli" in sys.argv:
        run_cli()
    else:
        from payment_system.gui import run
        run()


if __name__ == "__main__":
    main()
