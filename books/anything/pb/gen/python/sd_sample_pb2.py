# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sd-sample.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsd-sample.proto\x12\x0esample.pien.v1\"\x8d\x01\n\rSampleRequest\x12\x18\n\x07message\x18\x01 \x01(\tR\x07message\x1a\x62\n\x06Option\x12\x1e\n\x08sort_key\x18\x01 \x01(\tH\x00R\x07sortKey\x88\x01\x01\x12\x1e\n\x08sort_asc\x18\x02 \x01(\x08H\x01R\x07sortAsc\x88\x01\x01\x42\x0b\n\t_sort_keyB\x0b\n\t_sort_asc\"D\n\x0eSampleResponse\x12\x18\n\x07message\x18\x01 \x01(\tR\x07message\x12\x18\n\x07success\x18\x02 \x01(\x08R\x07success\"C\n\x0cLoginRequest\x12\x17\n\x07user_id\x18\x01 \x01(\tR\x06userId\x12\x1a\n\x08password\x18\x02 \x01(\tR\x08password\"%\n\rLoginResponse\x12\x14\n\x05token\x18\x01 \x01(\tR\x05token2\xa4\x01\n\rSampleService\x12M\n\x0cSampleMethod\x12\x1d.sample.pien.v1.SampleRequest\x1a\x1e.sample.pien.v1.SampleResponse\x12\x44\n\x05Login\x12\x1c.sample.pien.v1.LoginRequest\x1a\x1d.sample.pien.v1.LoginResponseB\xa0\x01\n\x12\x63om.sample.pien.v1B\rSdSampleProtoP\x01Z!github.com/kokoichi206/til;pienv1\xa2\x02\x03SPX\xaa\x02\x0eSample.Pien.V1\xca\x02\x0eSample\\Pien\\V1\xe2\x02\x1aSample\\Pien\\V1\\GPBMetadata\xea\x02\x10Sample::Pien::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sd_sample_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\022com.sample.pien.v1B\rSdSampleProtoP\001Z!github.com/kokoichi206/til;pienv1\242\002\003SPX\252\002\016Sample.Pien.V1\312\002\016Sample\\Pien\\V1\342\002\032Sample\\Pien\\V1\\GPBMetadata\352\002\020Sample::Pien::V1'
  _globals['_SAMPLEREQUEST']._serialized_start=36
  _globals['_SAMPLEREQUEST']._serialized_end=177
  _globals['_SAMPLEREQUEST_OPTION']._serialized_start=79
  _globals['_SAMPLEREQUEST_OPTION']._serialized_end=177
  _globals['_SAMPLERESPONSE']._serialized_start=179
  _globals['_SAMPLERESPONSE']._serialized_end=247
  _globals['_LOGINREQUEST']._serialized_start=249
  _globals['_LOGINREQUEST']._serialized_end=316
  _globals['_LOGINRESPONSE']._serialized_start=318
  _globals['_LOGINRESPONSE']._serialized_end=355
  _globals['_SAMPLESERVICE']._serialized_start=358
  _globals['_SAMPLESERVICE']._serialized_end=522
# @@protoc_insertion_point(module_scope)