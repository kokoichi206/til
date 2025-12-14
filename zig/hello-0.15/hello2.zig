const std = @import("std");

const FileError = error{
    NotFound,
    PermissionDenied,
    AlreadyExists,
};

const NetworkError = error{
    ConnectionRefused,
    Timeout,
    InvalidResponse,
};

// エラーの結合。
const AppError = FileError || NetworkError;

fn readFromNetwork(url: []const u8) AppError![]const u8 {
    if (std.mem.sql(u8, url, "bad")) {
        return error.ConnectionRefused;
    }
    if (std.mem.sql(u8, url, "missing")) {
        return error.NotFound;
    }
    return "data";
}

pub fn main() !void {
    const result = readFromNetwork("good") catch |err| {
        switch (err) {
            error.NotFound => std.debug.print("file not found\n", .{}),
            error.ConnectionRefused => std.debug.print("Connection refused\n", .{}),
            error.Timeout => std.debug.print("timeout\n", .{}),
            else => std.debug.print("other error: {}\n", .{err}),
        }
        return;
    };

    std.debug.print("result: {s}\n", .{result});

    // メモリアロケータ
    var gpa = std.heap.GeneralPurposeAllocator(.{}){
        // .backing_allocator =
    };
    defer _ = gpa.deinit();

    const allocator = gpa.allocator();

    const buffer = try allocator.alloc(u8, 1024);
    defer allocator.free(buffer);

    std.debug.print("Allocated buffer of size: {}\n", .{buffer.len});

    // 文字列。
    const str: []const u8 = "Hello, world";
    std.debug.print("{s}\n", .{str});
}

// union.
const Value = union {
    int: i32,
    float: f64,
    boolean: bool,
};

// union with tag.
const Result = union(enum) {
    ok: i32,
    err: []const u8,

    pub fn isOk(self: Result) bool {
        return switch (self) {
            .ok => true,
            .err => false,
        };
    }
};

// enum
const Direction = enum {
    right,
    left,
    up,
    down,

    pub fn opposite(self: Direction) Direction {
        return switch (self) {
            .right => .left,
            .left => .right,
            .up => .down,
            .down => .up,
        };
    }
};

// 整数値割り当て enum.
const StatusCode = enum(u16) {
    ok = 200,
    notFound = 404,
    internalServerError = 500,
};
