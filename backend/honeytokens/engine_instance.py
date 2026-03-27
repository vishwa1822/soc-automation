from honeytokens.honeytoken_engine import HoneytokenEngine
from honeytokens.trap_registry import TrapRegistry


# Single shared registry + engine instance used across the backend
_shared_registry = TrapRegistry()
honeytoken_engine = HoneytokenEngine(registry=_shared_registry)

