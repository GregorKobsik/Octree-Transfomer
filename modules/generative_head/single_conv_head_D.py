import torch.nn as nn


class SingleConvolutionalHeadD(nn.Module):
    def __init__(self, num_vocab, embed_dim, spatial_dim):
        """ Performs a convolutional transformation from transformer latent space into target value logits.

        Note: The token value '0' is reserved as a padding value, which does not propagate gradients.

        Args:
            num_vocab: Number of different target token values (exclusive padding token '0').
            embded_dim: Dimension of the latent embedding space of the transformer.
            spatial_dim: Spatial dimension (2D/3D) of the sequence data.
        """
        super(SingleConvolutionalHeadD, self).__init__()
        self.spatial_dim = spatial_dim
        e_dim = embed_dim
        layers = []

        # de-convolutions
        for _ in range(spatial_dim):
            layers.append(nn.ConvTranspose1d(e_dim, e_dim // 2, kernel_size=2, stride=2))
            layers.append(nn.GELU())
            e_dim = e_dim // 2
        self.value_deconvolution = nn.Sequential(*layers)

        # linear head
        self.linear = nn.Linear(e_dim, num_vocab + 1, bias=True)

    def _deconvolute(self, x):
        """ Deconvolutes given sequence, creating new tokens and reducing the emebdding dimension. """
        x = x.transpose(1, 2)
        x = self.value_deconvolution(x)
        return x.transpose(1, 2)

    def forward(self, x, value, depth, pos):
        """ Transforms the output of the transformer target value logits.

        Args:
            x: Output of the transformer, the latent vector [N, T', E].
            value: Target value token sequence [N, T].
            depth: Target depth token sequence [N, T].
            pos: Target position token sequence [N, T, A].

        Return
            Logits of target value sequence.
        """
        # deconvolute the latent space - create new tokens
        x = self._deconvolute(x)  # [N, T, E']

        # compute logits for each token
        return self.linear(x)  # [N, T, V]
