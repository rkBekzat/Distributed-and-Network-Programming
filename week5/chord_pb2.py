# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chord.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x63hord.proto\"\x07\n\x05\x45mpty\"/\n\x13ResponseFingerTable\x12\x18\n\x06result\x18\x01 \x03(\x0b\x32\x08.Address\"(\n\x0bRequestSave\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"-\n\x0eResponseAction\x12\n\n\x02ok\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1c\n\rRequestRemove\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1a\n\x0bRequestFind\x12\x0b\n\x03key\x18\x01 \x01(\t\"/\n\x0fRequestRegister\x12\x0e\n\x06ipaddr\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x03\"1\n\x10ResponseRegister\x12\x0c\n\x04\x64one\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1f\n\x11RequestDeregister\x12\n\n\x02id\x18\x01 \x01(\x03\"3\n\x12ResponseDeregister\x12\x0c\n\x04\x64one\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"(\n\x1aRequestPopulateFingerTable\x12\n\n\x02id\x18\x01 \x01(\x03\"#\n\x07\x41\x64\x64ress\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\"C\n\x1bResponsePopulateFingerTable\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x18\n\x06result\x18\x02 \x03(\x0b\x32\x08.Address\",\n\x10ResponseGetChord\x12\x18\n\x06result\x18\x01 \x03(\x0b\x32\x08.Address2\xb4\x01\n\x04Node\x12/\n\x0fGetFinger_table\x12\x06.Empty\x1a\x14.ResponseFingerTable\x12)\n\x08SaveData\x12\x0c.RequestSave\x1a\x0f.ResponseAction\x12)\n\x06Remove\x12\x0e.RequestRemove\x1a\x0f.ResponseAction\x12%\n\x04\x46ind\x12\x0c.RequestFind\x1a\x0f.ResponseAction2\xef\x01\n\x08Register\x12/\n\x08Register\x12\x10.RequestRegister\x1a\x11.ResponseRegister\x12\x35\n\nDeregister\x12\x12.RequestDeregister\x1a\x13.ResponseDeregister\x12P\n\x13PopulateFingerTable\x12\x1b.RequestPopulateFingerTable\x1a\x1c.ResponsePopulateFingerTable\x12)\n\x0cGetChordInfo\x12\x06.Empty\x1a\x11.ResponseGetChordb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chord_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=15
  _EMPTY._serialized_end=22
  _RESPONSEFINGERTABLE._serialized_start=24
  _RESPONSEFINGERTABLE._serialized_end=71
  _REQUESTSAVE._serialized_start=73
  _REQUESTSAVE._serialized_end=113
  _RESPONSEACTION._serialized_start=115
  _RESPONSEACTION._serialized_end=160
  _REQUESTREMOVE._serialized_start=162
  _REQUESTREMOVE._serialized_end=190
  _REQUESTFIND._serialized_start=192
  _REQUESTFIND._serialized_end=218
  _REQUESTREGISTER._serialized_start=220
  _REQUESTREGISTER._serialized_end=267
  _RESPONSEREGISTER._serialized_start=269
  _RESPONSEREGISTER._serialized_end=318
  _REQUESTDEREGISTER._serialized_start=320
  _REQUESTDEREGISTER._serialized_end=351
  _RESPONSEDEREGISTER._serialized_start=353
  _RESPONSEDEREGISTER._serialized_end=404
  _REQUESTPOPULATEFINGERTABLE._serialized_start=406
  _REQUESTPOPULATEFINGERTABLE._serialized_end=446
  _ADDRESS._serialized_start=448
  _ADDRESS._serialized_end=483
  _RESPONSEPOPULATEFINGERTABLE._serialized_start=485
  _RESPONSEPOPULATEFINGERTABLE._serialized_end=552
  _RESPONSEGETCHORD._serialized_start=554
  _RESPONSEGETCHORD._serialized_end=598
  _NODE._serialized_start=601
  _NODE._serialized_end=781
  _REGISTER._serialized_start=784
  _REGISTER._serialized_end=1023
# @@protoc_insertion_point(module_scope)
