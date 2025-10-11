def handler(ctx, data: bytes=None):
    name = "World"
    if data:
        try:
            name = data.decode("utf-8") or name
        except Exception:
            pass
    return f"Hello, {name}!"
