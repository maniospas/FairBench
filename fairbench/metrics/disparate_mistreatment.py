from fairbench.fork import parallel
from eagerpy import Tensor
from typing import Optional


@parallel
def dfpr(
    predictions: Tensor,
    labels: Tensor,
    sensitive: Tensor,
    non_sensitive: Optional[Tensor] = None,
):
    if non_sensitive is None:
        non_sensitive = 1.0 - sensitive
    error = (predictions - labels).abs() * predictions
    error_sensitive = error * sensitive
    error_non_sensitive = error * non_sensitive
    num_sensitive = (sensitive * predictions).sum()
    num_non_sensitive = (non_sensitive * predictions).sum()
    return (
        error_sensitive.sum() / num_sensitive
        - error_non_sensitive.sum() / num_non_sensitive
    )


@parallel
def dfnr(
    predictions: Tensor,
    labels: Tensor,
    sensitive: Tensor,
    non_sensitive: Optional[Tensor] = None,
    max_prediction: float = 1,
):
    negatives = max_prediction - predictions
    if non_sensitive is None:
        non_sensitive = 1.0 - sensitive
    error = (predictions - labels).abs() * negatives
    error_sensitive = error * sensitive
    error_non_sensitive = error * non_sensitive
    num_sensitive = (sensitive * negatives).sum()
    num_non_sensitive = (non_sensitive * negatives).sum()
    if num_sensitive == 0 or num_non_sensitive == 0:
        return 0
    return (
        error_sensitive.sum() / num_sensitive
        - error_non_sensitive.sum() / num_non_sensitive
    )
