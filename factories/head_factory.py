from modules.generative_head import (
    LinearHead,
    SingleConvolutionalHeadA,
    SingleConvolutionalHeadB,
    SingleConvolutionalHeadC,
    SingleConvolutionalHeadD,
    SplitHeadA,
    SplitHeadB,
    DoubleConvolutionalHead,
)


def create_head(name, num_vocab, embed_dim, spatial_dim):
    """ Creates a generative head.

    If the module specified in `name` does not exist raises a value error.

    Args:
        name: Defines which generative head will be created.
        num_vocab: Number of different vocabs in the vocabulary set.
        embed_dim: Size of embedding dimensions used by the transformer model.
        spatial_dim: Spatial dimensionality of input data.

    Return:
        Generative head initialised with specified parameters.
    """
    if name in ('generative_basic', 'linear'):
        return LinearHead(num_vocab, embed_dim)
    elif name in ('single_conv', 'single_conv_A'):
        return SingleConvolutionalHeadA(num_vocab, embed_dim, spatial_dim)
    elif name == 'single_conv_B':
        return SingleConvolutionalHeadB(num_vocab, embed_dim, spatial_dim)
    elif name == 'single_conv_C':
        return SingleConvolutionalHeadC(num_vocab, embed_dim, spatial_dim)
    elif name == 'single_conv_D':
        return SingleConvolutionalHeadD(num_vocab, embed_dim, spatial_dim)
    elif name == 'split_A':
        return SplitHeadA(num_vocab, embed_dim, spatial_dim)
    elif name == 'split_B':
        return SplitHeadB(num_vocab, embed_dim, spatial_dim)
    elif name == 'double_conv':
        return DoubleConvolutionalHead(num_vocab, embed_dim, spatial_dim)
    else:
        raise ValueError(f"ERROR: {name} head not implemented.")