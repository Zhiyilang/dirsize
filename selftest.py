import importlib
m = importlib.import_module("dirsize")
assert hasattr(m, "main") and callable(m.main), "main() missing in dirsize"
print("selftest OK: dirsize importable, main() callable")
