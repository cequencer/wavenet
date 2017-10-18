

| Lr/decay | Momentum/epsilon | Loss@100  | Acc@100   | MSE@100 | ETA@100 |
|-----------:|---------:|-------:|----------:|--------:|--------:|
|             1 |        5    |    3.1151 |    0.0016 |   16083 |   71416 |
|             5 |        5    |    2.9282 |    0.0015 |   16318 |   71035 |
|          0.99 |        0.99 |   14.0598 |    0.0047 |    3445 |   71204 |
|          0.25 |        0.9  |    5.2479 |    0.0100 |    4247 |   71026 |
|          0.40 |        0.9  |    5.2087 |    0.0105 |    3748 |   71172 |
|          0.60 |        0.9  |    5.3565 |    0.0070 |    5927 |   71043 |
|          0.15 |        0.9  |    5.3049 |    0.0089 |    5323 |   71423 |
|          0.33 |        0.9  |    5.3006 |    0.0069 |    4817 |   71193 |
|         0.30   |       0.99 |   11.6780 |    0.0075 |    6318 |   71235 |
|        a0.01  |      0.0001 |    5.2788 |    0.0081 |    5190 |   72354 |
|        a0.9   |      0.9    |    5.5508 |    0.0041 |    7465 |   72421 |
|       nadam   |       nadam |    4.7812 |    0.0200 |    1945 |   73505 |
|       adagrad |    adagrad  |    5.3843 |    0.0077 |    5832 |   71168 |
|      adadelta |    adadelta |    5.2701 |    0.0087 |    5261 |   72539 |
|        adamax |      adamax |    4.5812 |    0.0260 |    2074 |   71656 |
|       rmsprop |     rmsprop |    4.7300 |    0.0216 |    1956 |   71105 |
|    nadam@300   |         300 |    4.3125 |    0.0313 |    1052 |   69092 |
|   rmsprop@300 |         300 |    4.2951 |    0.0322 |    1111 |   68614 |
|  rmsprop@1000 |        1000 |    3.8559 |    0.0481 |     585 |   67184 |

10-18 17:04:02.253456: W tensorflow/core/common_runtime/bfc_allocator.cc:217] Allocator (GPU_0_bfc) ran out of memory trying to allocate 2.66GiB. The caller indicates that this is not a failure, but may mean that there could be performance gains if more memory is available.
  1001/140352 [..............................] - ETA: 67184s - loss: 3.8559 - categorical_accuracy: 0.0481 - categorical_mean_squared_error: 585.1838
