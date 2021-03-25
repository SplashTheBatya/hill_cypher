import numpy as np

a = ord('а')

print(dict(list(enumerate(
    list(''.join([chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)]))))))
