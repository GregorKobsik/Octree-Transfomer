from torch.nn.utils.rnn import pad_sequence


class BasicPadding(object):
    def __init__(self, architecture):
        """ Creates a padding module, which pads batched sequences to equal length with the padding token '0'.

        Args:
            architecture: Defines whether the transformer uses a 'encoder_only' or 'encoder_decocer' architecture.
        """
        self.architecture = architecture

    def __call__(self, batch):
        """ Pads the sequence batch and packs it into required tuples.

        Note: Uses different output shapes for 'encoder_only' and 'encoder_decoder' architecture.

        Args:
            batch: List of transformed input sequences.

        Return:
            Tensor with padded sequences. The 'encoder_only' architecture has the shape (enc_input, target) and the
            'encoder_decoder' architecture has the shape (enc_input, dec_input, target), where 'enc/dec_input' consists
            of a (value, depth, target) tuple for the encoder or decoder, respectively.
        """
        if self.architecture == "encoder_only":
            return self.encoder_only(batch)
        elif self.architecture == "encoder_decoder":
            return self.encoder_decoder(batch)
        else:
            print(f"ERROR: No padding function implemented for {self.architecture}")
            raise ValueError

    def encoder_only(self, batch):
        """ Pads and packs a list of samples for the 'encoder_only' architecture. """
        # unpack batched sequences
        value, depth, position, target = zip(*batch)

        # pad each batched sequences with '0' to same length
        value_pad = pad_sequence(value, batch_first=True, padding_value=0)
        depth_pad = pad_sequence(depth, batch_first=True, padding_value=0)
        pos_pad = pad_sequence(position, batch_first=True, padding_value=0)
        target_pad = pad_sequence(target, batch_first=True, padding_value=0)

        # return as (input, target)
        return (value_pad, depth_pad, pos_pad), target_pad

    def encoder_decoder(self, batch):
        """ Pads and packs a list of samples for the 'encoder_decoder' architecture. """
        # unpack batched sequences
        val_enc, dep_enc, pos_enc, val_dec, dep_dec, pos_dec, target = zip(*batch)

        # pad each batched sequences with '0' to same length
        v_enc_pad = pad_sequence(val_enc, batch_first=True, padding_value=0)
        d_enc_pad = pad_sequence(dep_enc, batch_first=True, padding_value=0)
        p_enc_pad = pad_sequence(pos_enc, batch_first=True, padding_value=0)
        v_dec_pad = pad_sequence(val_dec, batch_first=True, padding_value=0)
        d_dec_pad = pad_sequence(dep_dec, batch_first=True, padding_value=0)
        p_dec_pad = pad_sequence(pos_dec, batch_first=True, padding_value=0)
        target_pad = pad_sequence(target, batch_first=True, padding_value=0)

        # return as ((input_enc, input_dec), target)
        return ((v_enc_pad, d_enc_pad, p_enc_pad), (v_dec_pad, d_dec_pad, p_dec_pad)), target_pad