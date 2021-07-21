import torch

from tqdm.auto import trange


class SubstitutionGenerator():
    def __init__(self, compute_logits_fn, num_tokens=8, **_):
        """ Create token generator instance which samples 'num_tokens' in one pass.

        Args:
            compute_logits_fn: Pointer to function, which computes logits of given sequence.
            num_tokens: Defines the number of sampled tokens in each step.
        """
        self.compute_logits = compute_logits_fn
        self.num_tokens = num_tokens
        self.kernel_size = num_tokens

    def __call__(self, val, dep, pos, memory=None, idx=0, temperature=1.0, **_):
        """ Sample autoregressively current value token sequence and return updated value sequence.

        Args:
            val: Value token sequence of currently sampled layer.
            dep: Depth token sequence of currently sampled layer.
            pos: Position token sequence of currently sampled layer.
            memory: Latent sequence vector of the previous layer.
            idx: Currently sampled transformer layer index.
            temperature: Defines the randomness of the samples.

        Return:
            Sampled token sequence with values of the current layer.
        """
        # compute indices
        token_idx = 0
        start_idx = 0
        stop_idx = len(val[-2])
        sampled_idx = len(torch.cat(val[:-1]))

        # sample tokens autoregressively
        for prev_idx in trange(start_idx, stop_idx, self.kernel_size, leave=False, desc="Tokens"):
            # concat and pack token sequences
            seq = (torch.cat(val).unsqueeze(0), torch.cat(dep).unsqueeze(0), torch.cat(pos).unsqueeze(0))

            # compute logits
            logits = self.compute_logits(seq, memory, idx)[0]

            # compute number of sampled tokens
            num_sampled = torch.sum(val[-2][prev_idx:prev_idx + self.kernel_size] == 2) * self.num_tokens

            # retrive only logits for tokens which were actually sampled
            sampled_token_logits = logits[sampled_idx + token_idx:sampled_idx + token_idx + num_sampled]

            # check transformer token capacity
            if len(sampled_token_logits) != num_sampled:
                return val[-1][:token_idx]  # reached maximum number of tokens

            # compute token probabilities from logits
            probs = torch.nn.functional.softmax(sampled_token_logits / temperature, dim=-1)  # [t, V]
            probs[:, 0] = 0  # 'padding' token

            # sample next sequence token
            for i in range(len(probs)):
                val[-1][token_idx + i] = torch.multinomial(probs[i], num_samples=1)[0]
            token_idx += num_sampled

        return val[-1]