
from pydantic import BaseModel, Field
from typing import Literal


class TicketPrediction(BaseModel):

    ticket: str = Field(min_length=1)

    category: Literal[
        "Account",
        "Billing",
        "Bug",
        "Subscription",
        "API"
    ]

    priority: Literal[
        "High",
        "Medium",
        "Low"
    ]

    department: str
