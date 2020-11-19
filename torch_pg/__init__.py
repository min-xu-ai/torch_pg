import logging
import torch
import torch_pg._C as capi
import torch.distributed.distributed_c10d as c10d

try:
    import torch_pg._CUDA as cuda_api
except Exception:
    cuda_api = None
    pass

def init_mpi():
    class ProcessGroupMPI:
        pass

    ProcessGroupMPI.create = capi.createProcessGroupMPI
    c10d.ProcessGroupMPI = ProcessGroupMPI
    c10d._MPI_AVAILABLE = True

def init_nccl():
    if cuda_api is None:
        logging.warn("cannot initialize nccl, extension not built")
        return
    c10d.ProcessGroupNCCL = cuda_api.createProcessGroupNCCL
    c10d._NCCL_AVAILABLE = True
