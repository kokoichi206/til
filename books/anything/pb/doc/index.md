# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [proto/sd-sample.proto](#proto_sd-sample-proto)
    - [LoginRequest](#sample-pien-v1-LoginRequest)
    - [LoginResponse](#sample-pien-v1-LoginResponse)
    - [SampleRequest](#sample-pien-v1-SampleRequest)
    - [SampleRequest.Option](#sample-pien-v1-SampleRequest-Option)
    - [SampleResponse](#sample-pien-v1-SampleResponse)
  
    - [SampleService](#sample-pien-v1-SampleService)
  
- [Scalar Value Types](#scalar-value-types)



<a name="proto_sd-sample-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## proto/sd-sample.proto
サンプルサービスです。何も機能を提供していません。

ログイン情報はメタデータの JWT トークンで提供するため、引数には入りません。


<a name="sample-pien-v1-LoginRequest"></a>

### LoginRequest
ログインリクエストです。


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| user_id | [string](#string) |  | ユーザーIDです。 |
| password | [string](#string) |  | パスワードです。 |






<a name="sample-pien-v1-LoginResponse"></a>

### LoginResponse
ログインレスポンスです。


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| token | [string](#string) |  | JWTトークンです。 |






<a name="sample-pien-v1-SampleRequest"></a>

### SampleRequest
サンプルリクエストです。


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message | [string](#string) |  | メッセージです。 |






<a name="sample-pien-v1-SampleRequest-Option"></a>

### SampleRequest.Option



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sort_key | [string](#string) | optional | ソートキーです。 |
| sort_asc | [bool](#bool) | optional | 昇順フラグです。 |






<a name="sample-pien-v1-SampleResponse"></a>

### SampleResponse
サンプルレスポンスです。


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message | [string](#string) |  | メッセージです。 |
| success | [bool](#bool) |  | 成功フラグです。 |





 

 

 


<a name="sample-pien-v1-SampleService"></a>

### SampleService
サンプルサービスです。

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| SampleMethod | [SampleRequest](#sample-pien-v1-SampleRequest) | [SampleResponse](#sample-pien-v1-SampleResponse) | サンプルメソッドです。 |
| Login | [LoginRequest](#sample-pien-v1-LoginRequest) | [LoginResponse](#sample-pien-v1-LoginResponse) | ログインメソッドです。

- INVALID_ARGUMENT: 引数が不正な場合 - UNAUTHENTICATED: ログイン情報がない場合 |

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

