from functools import reduce
import torch
from torch.utils.data import DataLoader

class NullLoader(DataLoader):
    def __init__(self, proto_loader:DataLoader,
                 outbatch:int, rejection_iters:int, buffer_len:int,
                 reduced_shape:tuple[int], outshape:tuple[int],
                 dimreduction = lambda x: x,
                 device = 'cuda'):
        self.proto = proto_loader
        self.proto_batch = proto_loader.batch_size
        self.mem = buffer_len
        self.dimreduce = dimreduction
        self.rdim = reduced_shape
        self.odim = outshape
        self.batch_size = outbatch
        self.rejection_iters = rejection_iters
        self.device = device
        # assert outbatch % rejection_iters == 0, f"must be able to make full batch in {rejection_iters} iters"
        # assert self.mem % self.proto_batch == 0, f"buffer len {self.mem} must be divisible by the prototype loader batch size {self.proto_batch}"
        self.buffer = torch.zeros((self.mem,) + self.rdim, device=self.device)

    def __iter__(self):
        cand_labels = []
        candidates = []
        gradweights = []
        top_n = self.batch_size // self.rejection_iters

        for _ in range(self.rejection_iters):
            # print("rejection iter", _)
            self._protobatch, self._protolabels = next(iter(self.proto))
            self._protobatch, self._protolabels = self._protobatch.to(self.device), self._protolabels.to(self.device)
            dimreduced = self.dimreduce(self._protobatch)

            # Compute the SVD of the buffer
            U, S, Vh = torch.linalg.svd(self.buffer.view((self.mem, -1)), full_matrices=False)

            # Determine the rank and construct the projection matrix onto the null space
            threshold = 1e-6
            rank = (S > threshold).sum().item()
            if rank == 0:
                # The buffer is empty or has rank zero; the null space is the entire space
                P_null = torch.eye(self.buffer.shape[1], device=self.device)
            else:
                V_row = Vh[:rank, :]
                P_row = V_row.T @ V_row
                P_null = torch.eye(P_row.shape[0], device=self.device) - P_row

            # Project candidates onto the null space and compute projection errors
            dimreduced_flat = dimreduced.view(self._protobatch.size(0), -1).T  # Shape: (n_features, batch_size)
            projections = P_null.double() @ dimreduced_flat  # Shape: (n_features, batch_size)
            proj_errs = torch.linalg.norm(projections, dim=0)

            # Select top_n candidates with the largest projection errors
            asort = torch.argsort(proj_errs, descending=True).to(self.device)
            gradweights.append(proj_errs[asort])
            candidates.append(self._protobatch[asort])
            cand_labels.append(self._protolabels[asort])

            # Update the buffer
            self.buffer = torch.roll(self.buffer, shifts=top_n, dims=0)
            self.buffer[:top_n] = dimreduced[asort[:top_n]].float()

        # Concatenate and normalize gradweights
        candidates = torch.cat(candidates, dim=0)
        cand_labels = torch.cat(cand_labels, dim=0)
        gradweights = torch.cat(gradweights, dim=0)
        gradweights /= gradweights.sum()

        yield candidates, cand_labels, proj_errs, asort
