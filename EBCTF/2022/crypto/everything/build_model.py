# set up logging
import numba
import time
import pickle
import logging
from numba.pycc import CC


cc = CC('gpt')

import numpy as np

import math


@cc.export('sample', 'i8[:](i8[:], f4[:,:,::1], f4[:,::1])')
def sample(xx, ParamW, ParamB):

    block_size = 128
    for k in range(100):
        x_cond = xx[-block_size:]

        idx = np.ascontiguousarray(x_cond)
        x = ParamW[0].T[idx,:128] + ParamW[1].T[:len(idx), :128]
    
        K = 16
        for i in range(8):
            
            #ln = LayerNorm(2+i*K, x, ParamB, 128)
            dim = 128
            weight = ParamB[2+i*K][:dim]
            bias = ParamB[2+i*K+1][:dim]
            y =  (x - (x).sum(1).reshape((x.shape[0],1))/x.shape[1])
            v = y - (y).sum(1).reshape((x.shape[0],1))/y.shape[1]
            v = (v**2).sum(1).reshape((x.shape[0],1)) / (v.shape[1]-1)
            y /= np.sqrt(v + 1e-5)
            y *= weight
            y += bias
            ln = y

            # csa = CausalSelfAttention(6+i*K, ln, ParamW, ParamB)
            n_head = 8
            T, C = x.shape;

            def Linear(i, x, ParamW, ParamB, di, do):
                weight = ParamW[i][:di, :do]
                return x @ weight + ParamB[i+1][:do]
            
            k = Linear(6+i*K+0, ln, ParamW, ParamB, 128, 128).reshape((T, n_head, C // n_head)).transpose((1, 0, 2))
            q = Linear(6+i*K+2, ln, ParamW, ParamB, 128, 128).reshape((T, n_head, C // n_head)).transpose((1, 0, 2))
            v = Linear(6+i*K+4, ln, ParamW, ParamB, 128, 128).reshape((T, n_head, C // n_head)).transpose((1, 0, 2))

            def matmul(a, b):
                c = np.zeros((a.shape[0], a.shape[1], b.shape[2]), dtype=np.float32)
                for i in range(a.shape[0]):
                    c[i,:,:] = a[i] @ b[i]
                return c
            
            
            att = (matmul(q, k.transpose((0,2,1)))) / np.array(np.sqrt(k.shape[-1]),dtype=np.float32)
        
            mask = (1-np.tril(np.ones((1, T, T), dtype=np.float32))) * 100
            att -= mask# TODO
            
            ex = np.exp(att)# - x.max(1))
            att = ex / ex.sum(axis=2).reshape((ex.shape[0], ex.shape[1], 1))
            y = matmul(att, v)
            y = np.ascontiguousarray(y.transpose((1, 0, 2))).reshape((T, C))
        
            csa = Linear(6+i*K+6, y, ParamW, ParamB, 128, 128)
            
            x = x + csa

            #ln = LayerNorm(4+i*K, x, ParamB, 128)
            dim = 128
            weight = ParamB[4+i*K][:dim]
            bias = ParamB[4+i*K+1][:dim]
            y =  (x - (x).sum(1).reshape((x.shape[0],1))/x.shape[1])
            v = y - (y).sum(1).reshape((x.shape[0],1))/y.shape[1]
            v = (v**2).sum(1).reshape((x.shape[0],1)) / (v.shape[1]-1)
            y /= np.sqrt(v + 1e-5)
            y *= weight
            y += bias
            ln = y

            di, do = 128, 512
            weight = ParamW[14+i*K][:di, :do]
            lin = ln @ weight + ParamB[15+i*K][:do]
            
            z = np.maximum(lin, 0)
    
            x = np.ascontiguousarray(x) + Linear(16+i*K, np.ascontiguousarray(z), ParamW, ParamB, 512, 128)
        

        ## x = Layernorm(x)
        dim = 128
        i = 18+7*K
        weight = ParamB[i][:dim]
        bias = ParamB[i+1][:dim]
        y =  (x - (x).sum(1).reshape((x.shape[0],1))/x.shape[1])
        v = y - (y).sum(1).reshape((x.shape[0],1))/y.shape[1]
        v = (v**2).sum(1).reshape((x.shape[0],1)) / (v.shape[1]-1)
        y /= np.sqrt(v + 1e-5)
        y *= weight
        y += bias
        x = y

        ## logits = Linear(x)
        i = 20+7*K
        di, do = 128, 94
        weight = ParamW[i][:di, :do]
        logits = x @ weight + ParamB[i+1][:do]

        def softmax(x):
            ex = np.exp(x)# - x.max(1))
            return ex / ex.sum(axis=1).reshape((ex.shape[0], 1))
        
        probs = softmax(logits)
        probs = probs[-1, :]
        probs_sum = np.cumsum(probs)
        rint = np.random.random()
        ix = np.where(probs_sum > rint)[0][0]
        #ix = probs.argmax()
        xx = np.append(xx, ix)
        
    return xx

if __name__ == '__main__':
    cc.compile()

