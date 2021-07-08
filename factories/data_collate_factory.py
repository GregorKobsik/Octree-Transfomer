import math

from data.collate import (
    AutoencoderCollate,
    EncoderOnlyCollate,
    EncoderDecoderCollate,
    EncoderMultiDecoderCollate,
)


def create_data_collate(architecture, embeddings, resolution):
    """ Creates a data collate function.

    Args:
        architecture: Transformer architecture defines which data transformation function will be created.
        embedding: Defines the used token embedding of the shape transformer.
        resolution: Maximum side length of input data.

    Return:
        data transformation function initialised with specified parameters.
    """
    if architecture == "autoencoder":
        return AutoencoderCollate()
    if architecture == "encoder_only":
        return EncoderOnlyCollate()
    if architecture == "encoder_decoder":
        return EncoderDecoderCollate()
    if architecture == "encoder_multi_decoder":
        return EncoderMultiDecoderCollate(1 + int(math.log2(resolution)) - len(embeddings))
    else:
        raise ValueError(f"ERROR: No data collate for {architecture} available.")
