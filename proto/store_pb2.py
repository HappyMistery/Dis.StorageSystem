# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: store.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bstore.proto\x12\x10\x64istributedstore\"\x19\n\nVoteGetReq\x12\x0b\n\x03key\x18\x01 \x01(\t\"@\n\x0bVoteGetResp\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\t\x12\x11\n\tvote_size\x18\x03 \x01(\x05\"1\n\x0bVotePutResp\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x11\n\tvote_size\x18\x02 \x01(\x05\"(\n\nVotePutReq\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"*\n\x0e\x44iscoverMsgReq\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\x1f\n\x0f\x44iscoverMsgResp\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\"\n\x0f\x46inalCommitResp\x12\x0f\n\x07success\x18\x01 \x01(\x08\",\n\x0e\x46inalCommitReq\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\'\n\tCommitReq\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1d\n\nCommitResp\x12\x0f\n\x07success\x18\x01 \x01(\x08\"(\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1e\n\x0bPutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"+\n\x0bGetResponse\x12\r\n\x05value\x18\x01 \x01(\t\x12\r\n\x05\x66ound\x18\x02 \x01(\x08\"\"\n\x0fSlowdownRequest\x12\x0f\n\x07seconds\x18\x01 \x01(\x05\"#\n\x10SlowDownResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x10\n\x0eRestoreRequest\"\"\n\x0fRestoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty2\xb7\x05\n\rKeyValueStore\x12\x42\n\x03put\x12\x1c.distributedstore.PutRequest\x1a\x1d.distributedstore.PutResponse\x12\x42\n\x03get\x12\x1c.distributedstore.GetRequest\x1a\x1d.distributedstore.GetResponse\x12Q\n\x08slowDown\x12!.distributedstore.SlowdownRequest\x1a\".distributedstore.SlowDownResponse\x12N\n\x07restore\x12 .distributedstore.RestoreRequest\x1a!.distributedstore.RestoreResponse\x12\x43\n\x06\x63ommit\x12\x1b.distributedstore.CommitReq\x1a\x1c.distributedstore.CommitResp\x12R\n\x0b\x66inalCommit\x12 .distributedstore.FinalCommitReq\x1a!.distributedstore.FinalCommitResp\x12R\n\x0b\x64iscoverMsg\x12 .distributedstore.DiscoverMsgReq\x1a!.distributedstore.DiscoverMsgResp\x12\x46\n\x07votePut\x12\x1c.distributedstore.VotePutReq\x1a\x1d.distributedstore.VotePutResp\x12\x46\n\x07voteGet\x12\x1c.distributedstore.VoteGetReq\x1a\x1d.distributedstore.VoteGetRespb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'store_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VOTEGETREQ']._serialized_start=33
  _globals['_VOTEGETREQ']._serialized_end=58
  _globals['_VOTEGETRESP']._serialized_start=60
  _globals['_VOTEGETRESP']._serialized_end=124
  _globals['_VOTEPUTRESP']._serialized_start=126
  _globals['_VOTEPUTRESP']._serialized_end=175
  _globals['_VOTEPUTREQ']._serialized_start=177
  _globals['_VOTEPUTREQ']._serialized_end=217
  _globals['_DISCOVERMSGREQ']._serialized_start=219
  _globals['_DISCOVERMSGREQ']._serialized_end=261
  _globals['_DISCOVERMSGRESP']._serialized_start=263
  _globals['_DISCOVERMSGRESP']._serialized_end=294
  _globals['_FINALCOMMITRESP']._serialized_start=296
  _globals['_FINALCOMMITRESP']._serialized_end=330
  _globals['_FINALCOMMITREQ']._serialized_start=332
  _globals['_FINALCOMMITREQ']._serialized_end=376
  _globals['_COMMITREQ']._serialized_start=378
  _globals['_COMMITREQ']._serialized_end=417
  _globals['_COMMITRESP']._serialized_start=419
  _globals['_COMMITRESP']._serialized_end=448
  _globals['_PUTREQUEST']._serialized_start=450
  _globals['_PUTREQUEST']._serialized_end=490
  _globals['_PUTRESPONSE']._serialized_start=492
  _globals['_PUTRESPONSE']._serialized_end=522
  _globals['_GETREQUEST']._serialized_start=524
  _globals['_GETREQUEST']._serialized_end=549
  _globals['_GETRESPONSE']._serialized_start=551
  _globals['_GETRESPONSE']._serialized_end=594
  _globals['_SLOWDOWNREQUEST']._serialized_start=596
  _globals['_SLOWDOWNREQUEST']._serialized_end=630
  _globals['_SLOWDOWNRESPONSE']._serialized_start=632
  _globals['_SLOWDOWNRESPONSE']._serialized_end=667
  _globals['_RESTOREREQUEST']._serialized_start=669
  _globals['_RESTOREREQUEST']._serialized_end=685
  _globals['_RESTORERESPONSE']._serialized_start=687
  _globals['_RESTORERESPONSE']._serialized_end=721
  _globals['_EMPTY']._serialized_start=723
  _globals['_EMPTY']._serialized_end=730
  _globals['_KEYVALUESTORE']._serialized_start=733
  _globals['_KEYVALUESTORE']._serialized_end=1428
# @@protoc_insertion_point(module_scope)
