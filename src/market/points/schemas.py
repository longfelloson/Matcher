from pydantic import BaseModel, Field

from market.points.enums import PointsOperationType


class UpdateUserPoints(BaseModel):
    amount: int | float = Field(..., gt=0, description="Amount to change points by")
    operation: PointsOperationType
