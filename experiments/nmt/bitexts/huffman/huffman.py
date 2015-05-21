import sys
import re
import cPickle
from heapq import heappush, heappop, heapify

# DATA PREP:
# sed -i "s/ &apos;/'/g" [file-name].txt

M = 10000
F_NAME_PREFIX = None

def get_frequencies(f_name):
  freqs = {}
  with open(f_name, "r") as f:
    for line in f:
      for word in line.split():
        freqs[word] = freqs.setdefault(word, 0) + 1
  return freqs

def find_m_prime(freqs):
  m_prime = len(freqs) % (M - 1)
  return m_prime

def build_tree(freqs):
  # construct huffman tree
  heap = []
  m_prime = find_m_prime(freqs)
  for word, freq in freqs.items():
    heappush(heap, [freq, [word, ""]])
  count = 0
  while len(heap) > 1:
    elems = []
    for i in range(M if count > 0 else m_prime):
      curr = heappop(heap)
      for x in curr[1:]:
        x[1] = "s%d"%i + x[1]
      elems.append(curr)
    together = [sum(elem[0] for elem in elems)]
    for elem in elems:
      together.extend(elem[1:])
    heappush(heap, together)
    count += 1
  enc = dict(heappop(heap)[1:])
  # fix symbols
  for k, v in enc.items():
    if re.match("s[0-9]+s[0-9]+s", v):
      print "Symbol fixing will not work, tree depth > 2."
      sys.exit(1)
  symbol_map = {}
  for k, v in enc.items():
    if not re.match("s[0-9]+s", v):
      symbol_map[v] = k
      enc[k] = " " + k
  for k, v in enc.items():
    match = re.match("(s[0-9]+)(s[0-9]+)", v)
    if match:
      sym1, sym2 = match.groups()
      enc[k] = " " + sym1 + " " + (symbol_map[sym2] if sym2 in symbol_map else sym2)
  return enc

def reverse_dict(d):
  n = {}
  for k, v in d.items():
    n[v] = k
  return n

def construct_tree(f_name):
  freqs = get_frequencies(f_name)
  encoder = build_tree(freqs)
  decoder = reverse_dict(encoder)
  with open("%s_huff_enc.pkl"%F_NAME_PREFIX, "w") as f:
    cPickle.dump(encoder, f)
  with open("%s_huff_dec.pkl"%F_NAME_PREFIX, "w") as f:
    cPickle.dump(decoder, f)

def encode_from(f_name, enc_name):
  with open(enc_name, "r") as f:
    encoder = cPickle.load(f)
  with open(f_name, "r") as f, open("%s_encoded.txt"%F_NAME_PREFIX, "w") as f2:
    for line in f:
      to_write = ""
      for word in line.split():
        if word in encoder:
          to_write += encoder[word]
      f2.write(to_write + "\n")

def decode_from(f_name, dec_name):
  with open(dec_name, "r") as f:
    decoder = cPickle.load(f)
  with open(f_name, "r") as f, open("%s_decoded.txt"%F_NAME_PREFIX, "w") as f2:
    for line in f:
      curr = ""
      to_write = ""
      for word in line.split():
        curr += " " + word
        if curr in decoder:
          to_write += decoder[curr] + " "
          curr = ""
      f2.write(to_write[:-1] + "\n")

if __name__ == "__main__":
  usage = "python huffman.py [text file] [prefix] [pkl file (constructed if not given)] [-e (encode) or -d (decode)]"
  if len(sys.argv) not in (3, 5):
    print "Usage: %s"%usage
    sys.exit(1)
  F_NAME_PREFIX = sys.argv[2]
  if len(sys.argv) == 3:
    construct_tree(sys.argv[1])
  elif sys.argv[4] == "-e":
    encode_from(sys.argv[1], sys.argv[3])
  elif sys.argv[4] == "-d":
    decode_from(sys.argv[1], sys.argv[3])
  else:
    print "Usage: %s"%usage
    sys.exit(1)
