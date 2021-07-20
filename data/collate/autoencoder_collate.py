from .collate_utils import (
    get_min_batch_depth,
    pad_batch,
)


class AutoencoderCollate():
    def __init__(self, embeddings, resolution):
        """ Creates a collate module, which pads batched sequences to equal length with the padding token '0'.

        Args:
            embeddings: Defines the used token embeddings in the shape transformer.
        """
        self.embeddings = embeddings

    def __call__(self, batch):
        """ Pads and packs a list of samples for the 'autoencoder' architecture. """
        # get get the maximal usable depth value for every sample
        max_depth = get_min_batch_depth(batch)

        # select the lower (lo) and upper (up) layer depth bounds for the current embedding
        if self.embeddings[0] in ('substitution'):
            # select previous and last layer for 'substitution' embedding
            lo = max_depth - 1
            up = max_depth
        else:
            # get only a single depth layer
            lo = max_depth
            up = lo

        # extract value, depth and position sequences for each sample in batch
        batch = [(v[(lo <= d) & (d <= up)], d[(lo <= d) & (d <= up)], p[(lo <= d) & (d <= up)]) for v, d, p in batch]

        # pad sequences and return tensors
        seq_pad = pad_batch(batch)

        # return as (sequence, target)
        return seq_pad, seq_pad
