from fastapi import Header


async def current_user_id(x_user_id: str | None = Header(default=None)) -> str:
    """Local-friendly user resolver. Replace with JWT validation in production."""
    return x_user_id or "local-demo-user"
