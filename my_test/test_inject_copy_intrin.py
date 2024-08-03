import tvm
import tvm.testing
from tvm import te
from tvm.driver.build_module import schedule_to_module

def cb(src: tvm.tir.buffer, dst: tvm.tir.buffer, pad_before: tvm.ir.container.Array, 
  pad_after: tvm.ir.container.Array, pad_value: tvm.tir.expr.FloatImm):
  print("type of src: ", type(src))
  print("type of dst: ", type(dst))
  print("type of pad_before: ", type(pad_before))
  print("type of pad_after: ", type(pad_after))
  print("type of pad_value: ", type(pad_value))
  if (isinstance(src, tvm.tir.Buffer)):
    print("src is a buffer")
    print(f"The shape is: {src.shape}")
  tvm.testing.assert_prim_expr_equal(src.elem_offset, 0)
  assert pad_before[0].value == 1 # the size equals to the dimension of the buffer.
  assert pad_before[1].value == 0
  assert pad_after[0].value == 1
  assert pad_after[1].value == 0
  assert pad_value.value == 1.0
  return tvm.tir.Evaluate(0)

def test():
  m = te.var("m")
  l = te.var("l")
  A = te.placeholder((m, l), name="A")
  B = te.compute(
      (m + 2, l),
      lambda i, j: tvm.tir.if_then_else(tvm.tir.all(i >= 1, i < m + 1), A[i - 1, j], 1.0),
      name="B",
  )
  s = te.create_schedule(B.op)
  s[B].pragma(B.op.axis[0], "myself") # 0 is the first dimension, and 1 is the second dimension.
  print("TIR before transformation:")
  print(tvm.lower(s, [A, B]))
  
  mem_pass = tvm.tir.transform.InjectCopyIntrin("myself", cb)
  
  with tvm.transform.PassContext(config={"tir.add_lower_pass": [(1, mem_pass)]}):
    print("TIR after transformation:")
    print(tvm.lower(s, [A, B]))

if __name__ == "__main__":
  test()