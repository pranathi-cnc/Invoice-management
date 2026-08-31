from fastapi import Header, HTTPException
from pocketbase_service import pb


async def get_current_user(
    authorization: str = Header(None)
):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing."
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header."
        )

    token = authorization.replace("Bearer ", "")

    try:

        # Store JWT inside PocketBase client
        pb.auth_store.save(token)

        # Verify token
        auth = pb.collection("users").auth_refresh()

        return auth.record

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token."
        )