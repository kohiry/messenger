from fastapi import HTTPException


def get_error_user_in_db() -> HTTPException:
    return HTTPException(status_code=401, detail="User actually created")


def get_error_user_not_create() -> HTTPException:
    return HTTPException(status_code=401, detail="Register User failed")


def get_404_user_not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="User not found")
