from modules.embedding import (
    BasicEmbeddingB,
    SingleConvolutionalEmbeddingA,
    ConcatEmbeddingB,
    SubstitutionEmbedding,
    HalfConvolutionalEmbeddingA,
    MultiConvolutionalEmbeddingA,
)


def create_embedding(name, num_vocab, embed_dim, resolution, spatial_dim):
    """ Creates a token embedding.

    If the module specified in `name` does not exist raises a value error.

    Args:
        name: Defines which token embedding will be created.
        num_vocab: Number of different vocabs in the vocabulary set.
        embed_dim: Size of embedding dimensions used by the transformer model.
        resolution: Maximum side length of input data.
        spatial_dim: Spatial dimensionality of input data.

    Return:
        Token embedding initialised with specified parameters.
    """

    if name == 'basic_B':
        return BasicEmbeddingB(num_vocab, embed_dim, resolution, spatial_dim)
    elif name in ('single_conv', 'single_conv_A'):
        return SingleConvolutionalEmbeddingA(num_vocab, embed_dim, resolution, spatial_dim)
    elif name == 'concat_B':
        return ConcatEmbeddingB(num_vocab, embed_dim, resolution, spatial_dim)
    elif name == 'substitution':
        return SubstitutionEmbedding(num_vocab, embed_dim, resolution, spatial_dim)
    elif name == 'discrete_transformation':
        return BasicEmbeddingB(num_vocab**2**spatial_dim + 1, embed_dim, resolution, spatial_dim)
    elif name == 'half_conv_A':
        return HalfConvolutionalEmbeddingA(num_vocab, embed_dim, resolution, spatial_dim)
    elif name == 'multi_conv_A':
        return MultiConvolutionalEmbeddingA(num_vocab, embed_dim, resolution, spatial_dim)
    else:
        raise ValueError(f"ERROR: {name} embedding not implemented.")
