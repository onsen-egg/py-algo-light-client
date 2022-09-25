import ast

def process(s):
  return bytes(ast.literal_eval(",".join(s.split())))

# Int serialization logic
# x should be represented by n bytes (big-endian) where n is the 
# minimum number of bytes needed, and n=2^i.
# If n>=2, there is also a prepended byte 0xcc + i
def custom_int_serialize(x: int) -> bytes:
  assert(x > 0)
  i = next_power_of_2((x.bit_length() + 7) // 8)

  ret = b''
  if i > 0:
    ret += (0xcc + i).to_bytes(1, 'big')
  ret += x.to_bytes(1 << i, 'big')

  return ret

# Returns an i such that 2^i is the minimal
# power of 2 greater than or equal to n
def next_power_of_2(n):
  i = 0
  while n > 1<<i:
    i += 1
  return i

def serialize_block_header(
  seed: bytes,
  genesis_hash: bytes,
  round_number: int,
  tx_commitment: bytes
) -> bytes:
  lbh = bytes.fromhex('84' if round_number != 0 else '83')

  lbh += bytes.fromhex('a1')
  lbh += '0'.encode()
  lbh += bytes.fromhex('c420')
  lbh += seed

  lbh += bytes.fromhex('a2')
  lbh += 'gh'.encode()
  lbh += bytes.fromhex('c420')
  lbh += genesis_hash

  if round_number != 0:
    lbh += bytes.fromhex('a1')
    lbh += 'r'.encode()
    lbh += custom_int_serialize(round_number)

  lbh += bytes.fromhex('a2')
  lbh += 'tc'.encode()
  lbh += bytes.fromhex('c420')
  lbh += tx_commitment

  return lbh


if __name__ == '__main__':
  seed = bytes([137, 1, 173, 204, 51, 42, 78, 122, 215, 235, 52, 130, 57, 11, 137, 176, 62, 20, 53, 9, 223, 176, 146, 173, 149, 144, 110, 244, 121, 102, 48, 45])

  genesis_hash = bytes([202, 40, 44, 92, 151, 152, 244, 20, 69, 75, 39, 34, 53, 161, 88, 190, 148, 230, 239, 223, 36, 118, 191, 179, 84, 136, 79, 110, 153, 214, 167, 95])

  # round_number = 0x0
  round_number = 9

  tx_commitment = bytes([82, 95, 217, 45, 118, 45, 86, 230, 150, 70, 86, 29, 117, 241, 52, 225, 126, 144, 251, 104, 39, 213, 168, 163, 244, 124, 36, 131, 165, 155, 8, 166])

  lbh = serialize_block_header(
    seed,
    genesis_hash,
    round_number,
    tx_commitment
  )

  correct_bytes = bytes([132, 161, 48, 196, 32, 137, 1, 173, 204, 51, 42, 78, 122, 215, 235, 52, 130, 57, 11, 137, 176, 62, 20, 53, 9, 223, 176, 146, 173, 149, 144, 110, 244, 121, 102, 48, 45, 162, 103, 104, 196, 32, 202, 40, 44, 92, 151, 152, 244, 20, 69, 75, 39, 34, 53, 161, 88, 190, 148, 230, 239, 223, 36, 118, 191, 179, 84, 136, 79, 110, 153, 214, 167, 95, 161, 114, 9, 162, 116, 99, 196, 32, 82, 95, 217, 45, 118, 45, 86, 230, 150, 70, 86, 29, 117, 241, 52, 225, 126, 144, 251, 104, 39, 213, 168, 163, 244, 124, 36, 131, 165, 155, 8, 166])
  # correct_bytes = process('[132 161 48 196 32 137 1 173 204 51 42 78 122 215 235 52 130 57 11 137 176 62 20 53 9 223 176 146 173 149 144 110 244 121 102 48 45 162 103 104 196 32 202 40 44 92 151 152 244 20 69 75 39 34 53 161 88 190 148 230 239 223 36 118 191 179 84 136 79 110 153 214 167 95 161 114 207 0 0 0 17 34 51 68 85 162 116 99 196 32 82 95 217 45 118 45 86 230 150 70 86 29 117 241 52 225 126 144 251 104 39 213 168 163 244 124 36 131 165 155 8 166]')
  # correct_bytes = bytes.fromhex("83a130c4208901adcc332a4e7ad7eb3482390b89b03e143509dfb092ad95906ef47966302da26768c420ca282c5c9798f414454b272235a158be94e6efdf2476bfb354884f6e99d6a75fa27463c420525fd92d762d56e69646561d75f134e17e90fb6827d5a8a3f47c2483a59b08a6")

  assert(lbh == correct_bytes)
