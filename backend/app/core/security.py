from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass(frozen=True)
class RequestIdentity:
    user_id: str
    workspace_id: str
    role: str

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


async def current_identity(
    x_user_id: str | None = Header(default=None),
    x_workspace_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> RequestIdentity:
    """Resolve the local demo identity at the API boundary.

    Production deployments must replace trusted headers at the gateway with
    verified JWT claims. Keeping this resolver explicit prevents resource
    handlers from silently bypassing workspace authorization.
    """
    role = (x_user_role or "member").lower()
    if role not in {"member", "admin"}:
        raise HTTPException(status_code=400, detail="Unsupported user role")
    return RequestIdentity(
        user_id=x_user_id or "local-demo-user",
        workspace_id=x_workspace_id or "local-demo",
        role=role,
    )


async def current_user_id(x_user_id: str | None = Header(default=None)) -> str:
    """Local-friendly user resolver. Replace with JWT validation in production."""
    return x_user_id or "local-demo-user"
