"""Health check schemas."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status", json_schema_extra={"example": "ok"})
    version: str = Field(..., description="Service version", json_schema_extra={"example": "0.1.0"})
