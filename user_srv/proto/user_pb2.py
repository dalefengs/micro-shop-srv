# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='user.proto',
  package='',
  syntax='proto3',
  serialized_options=b'Z\010/.;proto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\nuser.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x1f\n\rMobileRequest\x12\x0e\n\x06mobile\x18\x01 \x01(\t\"\x17\n\tIdRequest\x12\n\n\x02id\x18\x01 \x01(\r\"N\n\x11\x43heckPasswordInfo\x12\x0e\n\x06mobile\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x17\n\x0f\x65ncryptPassword\x18\x03 \x01(\t\" \n\rCheckResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x98\x01\n\x10UserInfoResponse\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0e\n\x06mobile\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x10\n\x08nickname\x18\x04 \x01(\t\x12\x0e\n\x06gender\x18\x05 \x01(\x05\x12\x10\n\x08\x62irthday\x18\x06 \x01(\x04\x12\x0f\n\x07headUrl\x18\x07 \x01(\t\x12\x11\n\torangeKey\x18\x08 \x01(\t\"D\n\x0e\x43reateUserInfo\x12\x0e\n\x06mobile\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x10\n\x08nickname\x18\x03 \x01(\t\"\x90\x01\n\x08UserInfo\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0e\n\x06mobile\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x10\n\x08nickname\x18\x04 \x01(\t\x12\x0e\n\x06gender\x18\x05 \x01(\x05\x12\x10\n\x08\x62irthday\x18\x06 \x01(\x04\x12\x0f\n\x07headUrl\x18\x07 \x01(\t\x12\x11\n\torangeKey\x18\x08 \x01(\t\"\'\n\x08PageInfo\x12\x0c\n\x04page\x18\x01 \x01(\r\x12\r\n\x05limit\x18\x02 \x01(\r\"B\n\x10UserListResponse\x12\r\n\x05total\x18\x01 \x01(\r\x12\x1f\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x11.UserInfoResponse2\xb7\x02\n\x04User\x12\x38\n\x13GetUserInfoByMobile\x12\x0e.MobileRequest\x1a\x11.UserInfoResponse\x12\x30\n\x0fGetUserInfoById\x12\n.IdRequest\x1a\x11.UserInfoResponse\x12+\n\x0bGetUserList\x12\t.PageInfo\x1a\x11.UserListResponse\x12\x30\n\nCreateUser\x12\x0f.CreateUserInfo\x1a\x11.UserInfoResponse\x12/\n\nUpdateUser\x12\t.UserInfo\x1a\x16.google.protobuf.Empty\x12\x33\n\rCheckPassword\x12\x12.CheckPasswordInfo\x1a\x0e.CheckResponseB\nZ\x08/.;protob\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_MOBILEREQUEST = _descriptor.Descriptor(
  name='MobileRequest',
  full_name='MobileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mobile', full_name='MobileRequest.mobile', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=43,
  serialized_end=74,
)


_IDREQUEST = _descriptor.Descriptor(
  name='IdRequest',
  full_name='IdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='IdRequest.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=99,
)


_CHECKPASSWORDINFO = _descriptor.Descriptor(
  name='CheckPasswordInfo',
  full_name='CheckPasswordInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mobile', full_name='CheckPasswordInfo.mobile', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='CheckPasswordInfo.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encryptPassword', full_name='CheckPasswordInfo.encryptPassword', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=179,
)


_CHECKRESPONSE = _descriptor.Descriptor(
  name='CheckResponse',
  full_name='CheckResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='CheckResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=181,
  serialized_end=213,
)


_USERINFORESPONSE = _descriptor.Descriptor(
  name='UserInfoResponse',
  full_name='UserInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='UserInfoResponse.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mobile', full_name='UserInfoResponse.mobile', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='UserInfoResponse.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='UserInfoResponse.nickname', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gender', full_name='UserInfoResponse.gender', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='birthday', full_name='UserInfoResponse.birthday', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='headUrl', full_name='UserInfoResponse.headUrl', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orangeKey', full_name='UserInfoResponse.orangeKey', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=216,
  serialized_end=368,
)


_CREATEUSERINFO = _descriptor.Descriptor(
  name='CreateUserInfo',
  full_name='CreateUserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mobile', full_name='CreateUserInfo.mobile', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='CreateUserInfo.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='CreateUserInfo.nickname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=370,
  serialized_end=438,
)


_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='UserInfo.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mobile', full_name='UserInfo.mobile', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='UserInfo.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='UserInfo.nickname', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gender', full_name='UserInfo.gender', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='birthday', full_name='UserInfo.birthday', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='headUrl', full_name='UserInfo.headUrl', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orangeKey', full_name='UserInfo.orangeKey', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=441,
  serialized_end=585,
)


_PAGEINFO = _descriptor.Descriptor(
  name='PageInfo',
  full_name='PageInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='page', full_name='PageInfo.page', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='PageInfo.limit', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=587,
  serialized_end=626,
)


_USERLISTRESPONSE = _descriptor.Descriptor(
  name='UserListResponse',
  full_name='UserListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='total', full_name='UserListResponse.total', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='UserListResponse.data', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=628,
  serialized_end=694,
)

_USERLISTRESPONSE.fields_by_name['data'].message_type = _USERINFORESPONSE
DESCRIPTOR.message_types_by_name['MobileRequest'] = _MOBILEREQUEST
DESCRIPTOR.message_types_by_name['IdRequest'] = _IDREQUEST
DESCRIPTOR.message_types_by_name['CheckPasswordInfo'] = _CHECKPASSWORDINFO
DESCRIPTOR.message_types_by_name['CheckResponse'] = _CHECKRESPONSE
DESCRIPTOR.message_types_by_name['UserInfoResponse'] = _USERINFORESPONSE
DESCRIPTOR.message_types_by_name['CreateUserInfo'] = _CREATEUSERINFO
DESCRIPTOR.message_types_by_name['UserInfo'] = _USERINFO
DESCRIPTOR.message_types_by_name['PageInfo'] = _PAGEINFO
DESCRIPTOR.message_types_by_name['UserListResponse'] = _USERLISTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MobileRequest = _reflection.GeneratedProtocolMessageType('MobileRequest', (_message.Message,), {
  'DESCRIPTOR' : _MOBILEREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:MobileRequest)
  })
_sym_db.RegisterMessage(MobileRequest)

IdRequest = _reflection.GeneratedProtocolMessageType('IdRequest', (_message.Message,), {
  'DESCRIPTOR' : _IDREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:IdRequest)
  })
_sym_db.RegisterMessage(IdRequest)

CheckPasswordInfo = _reflection.GeneratedProtocolMessageType('CheckPasswordInfo', (_message.Message,), {
  'DESCRIPTOR' : _CHECKPASSWORDINFO,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:CheckPasswordInfo)
  })
_sym_db.RegisterMessage(CheckPasswordInfo)

CheckResponse = _reflection.GeneratedProtocolMessageType('CheckResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHECKRESPONSE,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:CheckResponse)
  })
_sym_db.RegisterMessage(CheckResponse)

UserInfoResponse = _reflection.GeneratedProtocolMessageType('UserInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERINFORESPONSE,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:UserInfoResponse)
  })
_sym_db.RegisterMessage(UserInfoResponse)

CreateUserInfo = _reflection.GeneratedProtocolMessageType('CreateUserInfo', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERINFO,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:CreateUserInfo)
  })
_sym_db.RegisterMessage(CreateUserInfo)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERINFO,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:UserInfo)
  })
_sym_db.RegisterMessage(UserInfo)

PageInfo = _reflection.GeneratedProtocolMessageType('PageInfo', (_message.Message,), {
  'DESCRIPTOR' : _PAGEINFO,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:PageInfo)
  })
_sym_db.RegisterMessage(PageInfo)

UserListResponse = _reflection.GeneratedProtocolMessageType('UserListResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERLISTRESPONSE,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:UserListResponse)
  })
_sym_db.RegisterMessage(UserListResponse)


DESCRIPTOR._options = None

_USER = _descriptor.ServiceDescriptor(
  name='User',
  full_name='User',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=697,
  serialized_end=1008,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetUserInfoByMobile',
    full_name='User.GetUserInfoByMobile',
    index=0,
    containing_service=None,
    input_type=_MOBILEREQUEST,
    output_type=_USERINFORESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetUserInfoById',
    full_name='User.GetUserInfoById',
    index=1,
    containing_service=None,
    input_type=_IDREQUEST,
    output_type=_USERINFORESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetUserList',
    full_name='User.GetUserList',
    index=2,
    containing_service=None,
    input_type=_PAGEINFO,
    output_type=_USERLISTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateUser',
    full_name='User.CreateUser',
    index=3,
    containing_service=None,
    input_type=_CREATEUSERINFO,
    output_type=_USERINFORESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateUser',
    full_name='User.UpdateUser',
    index=4,
    containing_service=None,
    input_type=_USERINFO,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CheckPassword',
    full_name='User.CheckPassword',
    index=5,
    containing_service=None,
    input_type=_CHECKPASSWORDINFO,
    output_type=_CHECKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USER)

DESCRIPTOR.services_by_name['User'] = _USER

# @@protoc_insertion_point(module_scope)
