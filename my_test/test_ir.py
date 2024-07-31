from tvm import te
import tvm
from tvm.ir.module import IRModule
from tvm.script import tir as T
import numpy as np

def test():
  A = te.placeholder((8,), dtype="float32", name="A")
  B = te.compute((8,), lambda i: A(i) + 1.0, name="B")
  func = te.create_prim_func([A, B])
  ir_module_from_te = IRModule({"main": func})
  print(ir_module_from_te.script())

if __name__ == "__main__":
  test()