from pydantic import BaseModel


class CapacityResponse(BaseModel):
    max_bytes: int
    max_kb: float
    dimensions: str


class GenerateKeyResponse(BaseModel):
    key: str


class DecodeResponse(BaseModel):
    text: str


class ErrorResponse(BaseModel):
    detail: str


class HealthResponse(BaseModel):
    status: str
    version: str
