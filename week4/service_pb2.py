# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\"\x1a\n\x07Message\x12\x0f\n\x07message\x18\x01 \x01(\t\".\n\rsplitResponse\x12\x0e\n\x06number\x18\x01 \x01(\x05\x12\r\n\x05parts\x18\x02 \x03(\t\"+\n\x0csplitRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05\x64\x65lim\x18\x02 \x01(\t\" \n\x0eisPrimeRequest\x12\x0e\n\x06number\x18\x01 \x01(\x05\x32|\n\tcalculate\x12\x1d\n\x07reverse\x12\x08.Message\x1a\x08.Message\x12&\n\x05split\x12\r.splitRequest\x1a\x0e.splitResponse\x12(\n\x07isprime\x12\x0f.isPrimeRequest\x1a\x08.Message(\x01\x30\x01\x62\x06proto3')



_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_SPLITRESPONSE = DESCRIPTOR.message_types_by_name['splitResponse']
_SPLITREQUEST = DESCRIPTOR.message_types_by_name['splitRequest']
_ISPRIMEREQUEST = DESCRIPTOR.message_types_by_name['isPrimeRequest']
Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  })
_sym_db.RegisterMessage(Message)

splitResponse = _reflection.GeneratedProtocolMessageType('splitResponse', (_message.Message,), {
  'DESCRIPTOR' : _SPLITRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:splitResponse)
  })
_sym_db.RegisterMessage(splitResponse)

splitRequest = _reflection.GeneratedProtocolMessageType('splitRequest', (_message.Message,), {
  'DESCRIPTOR' : _SPLITREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:splitRequest)
  })
_sym_db.RegisterMessage(splitRequest)

isPrimeRequest = _reflection.GeneratedProtocolMessageType('isPrimeRequest', (_message.Message,), {
  'DESCRIPTOR' : _ISPRIMEREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:isPrimeRequest)
  })
_sym_db.RegisterMessage(isPrimeRequest)

_CALCULATE = DESCRIPTOR.services_by_name['calculate']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=17
  _MESSAGE._serialized_end=43
  _SPLITRESPONSE._serialized_start=45
  _SPLITRESPONSE._serialized_end=91
  _SPLITREQUEST._serialized_start=93
  _SPLITREQUEST._serialized_end=136
  _ISPRIMEREQUEST._serialized_start=138
  _ISPRIMEREQUEST._serialized_end=170
  _CALCULATE._serialized_start=172
  _CALCULATE._serialized_end=296
# @@protoc_insertion_point(module_scope)
