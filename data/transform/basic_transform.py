import torch


class BasicTransform(object):
    def __init__(self, architecture):
        """ Creates a transform module, which transforms the input data samples for the 'basic' embedding.

        Args:
            architecture: Defines whether the transformer uses a 'encoder_only' or 'encoder_decocer' architecture.
        """
        self.architecture = architecture

    def __call__(self, value, depth, pos):
        """ Performs the transformation of a single sample sequence into the desired format.

        Note: Uses different output shapes for 'encoder_only' and 'encoder_decoder' architecture.

        Args:
            value: Raw value token sequence.
            depth: Raw depth token sequence.
            pos: Raw position token sequence.

        Return:
            Tuple representing the given sequences transformed to match the architecture requirements. The tuple has
            the shape (value, depth, pos, target) for the 'encoder_only' architecture and (enc_value, enc_depth,
            enc_pos, dec_value, dec_depth, dec_pos, target) for the 'encoder_decoder' architecture.
        """
        if self.architecture == "encoder_only":
            return self.encoder_only(value, depth, pos)
        elif self.architecture == "encoder_decoder":
            return self.encoder_decoder(value, depth, pos)
        else:
            print(f"ERROR: No transform function implemented for {self.architecture}")
            raise ValueError

    def encoder_only(self, value, depth, pos):
        """ Transforms a single sample for the 'encoder_only' architecture. """
        return torch.tensor(value), torch.tensor(depth), torch.tensor(pos), torch.tensor(value)

    def encoder_decoder(self, value, depth, pos):
        """ Transforms a single sample for the 'encoder_decoder' architecture. """
        # get maximum depth layer value
        max_depth = max(depth)

        # get all sequence layers, excepth last one
        val_enc = torch.tensor(value[depth != max_depth])
        dep_enc = torch.tensor(depth[depth != max_depth])
        pos_enc = torch.tensor(pos[depth != max_depth])

        # extract last sequence layer
        val_dec = torch.tensor(value[depth == max_depth])
        dep_dec = torch.tensor(depth[depth == max_depth])
        pos_dec = torch.tensor(pos[depth == max_depth])

        # target is the decoder input sequence
        target = val_dec.clone()

        # return sequences for encoder, decoder and target
        return val_enc, dep_enc, pos_enc, val_dec, dep_dec, pos_dec, target
