import torch.nn.functional as F

from torch.nn.modules.loss import _WeightedLoss

from torch import Tensor
from typing import Optional


class CrossEntropyLoss(_WeightedLoss):
    def __init__(
        self,
        weight: Optional[Tensor] = None,
        ignore_index: int = 0,
        **_,
    ) -> None:
        """ TODO: add description

        Args:
            weight:
            ignore_index:
            reduction:

        Return:

        """
        super(CrossEntropyLoss, self).__init__(weight, None, None, 'none')
        self.ignore_index = ignore_index

    def forward(self, logits: Tensor, target: Tensor) -> Tensor:
        """ TODO: add description

        Args:
            logits: [N, T, V]
            target: [N, T]

        Return:

        """
        # unpack target sequence
        tgt_val, _, _ = target  # [N, T]

        # flatten tensors
        input = logits.view(-1, logits.size(-1))  # [N*T, V]
        target = tgt_val.reshape(-1)  # [N*T]

        # compute cross entropy loss
        loss = F.cross_entropy(
            input, target, weight=self.weight, ignore_index=self.ignore_index, reduction=self.reduction
        )

        # return loss
        return loss.reshape(tgt_val.shape)  # [N, T]
