// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             (unknown)
// source: sd-sample.proto

package pienv1

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// SampleServiceClient is the client API for SampleService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type SampleServiceClient interface {
	// *
	// サンプルメソッドです。
	SampleMethod(ctx context.Context, in *SampleRequest, opts ...grpc.CallOption) (*SampleResponse, error)
	// *
	// ログインメソッドです。
	//
	// - INVALID_ARGUMENT: 引数が不正な場合
	// - UNAUTHENTICATED: ログイン情報がない場合
	Login(ctx context.Context, in *LoginRequest, opts ...grpc.CallOption) (*LoginResponse, error)
}

type sampleServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewSampleServiceClient(cc grpc.ClientConnInterface) SampleServiceClient {
	return &sampleServiceClient{cc}
}

func (c *sampleServiceClient) SampleMethod(ctx context.Context, in *SampleRequest, opts ...grpc.CallOption) (*SampleResponse, error) {
	out := new(SampleResponse)
	err := c.cc.Invoke(ctx, "/sample.pien.v1.SampleService/SampleMethod", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sampleServiceClient) Login(ctx context.Context, in *LoginRequest, opts ...grpc.CallOption) (*LoginResponse, error) {
	out := new(LoginResponse)
	err := c.cc.Invoke(ctx, "/sample.pien.v1.SampleService/Login", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// SampleServiceServer is the server API for SampleService service.
// All implementations should embed UnimplementedSampleServiceServer
// for forward compatibility
type SampleServiceServer interface {
	// *
	// サンプルメソッドです。
	SampleMethod(context.Context, *SampleRequest) (*SampleResponse, error)
	// *
	// ログインメソッドです。
	//
	// - INVALID_ARGUMENT: 引数が不正な場合
	// - UNAUTHENTICATED: ログイン情報がない場合
	Login(context.Context, *LoginRequest) (*LoginResponse, error)
}

// UnimplementedSampleServiceServer should be embedded to have forward compatible implementations.
type UnimplementedSampleServiceServer struct {
}

func (UnimplementedSampleServiceServer) SampleMethod(context.Context, *SampleRequest) (*SampleResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SampleMethod not implemented")
}
func (UnimplementedSampleServiceServer) Login(context.Context, *LoginRequest) (*LoginResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Login not implemented")
}

// UnsafeSampleServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to SampleServiceServer will
// result in compilation errors.
type UnsafeSampleServiceServer interface {
	mustEmbedUnimplementedSampleServiceServer()
}

func RegisterSampleServiceServer(s grpc.ServiceRegistrar, srv SampleServiceServer) {
	s.RegisterService(&SampleService_ServiceDesc, srv)
}

func _SampleService_SampleMethod_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SampleRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SampleServiceServer).SampleMethod(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/sample.pien.v1.SampleService/SampleMethod",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SampleServiceServer).SampleMethod(ctx, req.(*SampleRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _SampleService_Login_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(LoginRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SampleServiceServer).Login(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/sample.pien.v1.SampleService/Login",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SampleServiceServer).Login(ctx, req.(*LoginRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// SampleService_ServiceDesc is the grpc.ServiceDesc for SampleService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var SampleService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "sample.pien.v1.SampleService",
	HandlerType: (*SampleServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SampleMethod",
			Handler:    _SampleService_SampleMethod_Handler,
		},
		{
			MethodName: "Login",
			Handler:    _SampleService_Login_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "sd-sample.proto",
}