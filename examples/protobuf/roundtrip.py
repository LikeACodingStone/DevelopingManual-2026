"""Requires sample_pb2 generated from the adjacent new schema."""
from google.protobuf.message import DecodeError
from sample_pb2 import Sample

sample = Sample(channel=7, value=2.5, unit='V')
wire = sample.SerializeToString()
restored = Sample.FromString(wire)
assert restored == sample
# Truncated length-delimited field: the one-byte length varint never terminates.
try:
    Sample.FromString(bytes([0x1a, 0x80]))
except DecodeError:
    pass
else:
    raise AssertionError('malformed message accepted')
print('Protobuf roundtrip and malformed input OK')
