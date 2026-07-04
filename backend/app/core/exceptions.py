from fastapi import HTTPException, status


def api_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"data": None, "meta": {}, "errors": [{"code": code, "message": message}]})


UNAUTHORIZED = api_error(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED", "Authentication required.")
