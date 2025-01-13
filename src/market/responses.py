from fastapi.responses import JSONResponse
from fastapi import status


RESOURCE_CREATED_RESPONSE = JSONResponse(
    "Successfully created", status.HTTP_201_CREATED
)
RESOURCE_NOT_FOUND_RESPONSE = JSONResponse(
    "Resoruce not found", status.HTTP_404_NOT_FOUND
)
RESOURCE_UPDATED_RESPONSE = JSONResponse("Successfully updated")
RESOURCE_DELETED_RESPONSE = JSONResponse("Successfully deleted")
