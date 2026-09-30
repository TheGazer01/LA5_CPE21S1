"""payment_system: a deeply packaged demo of polymorphism."""
from payment_system.core.base import Payment
from payment_system.services.processor import PaymentProcessor

__all__ = ["Payment", "PaymentProcessor"]
