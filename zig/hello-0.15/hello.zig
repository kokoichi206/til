const std = @import("std");

// !void はエラーを返す可能性があることを示している。
// pub fn main がエントリーポイント。
// try でエラー伝播。
pub fn main() !void {
    std.debug.print("Hello, {s}\n", .{"worlddddd"});

    // defer!
    defer std.debug.print("Goodbye!\n", .{});
    // errdefer (エラー時のみ実行) もある！！

    const x: i32 = 10;

    // 型推論あり。
    // var y = 100;
    // y = 20;
    const y = 20;

    std.debug.print("x: {d}, y: {d}\n", .{ x, y });

    // comptime const xx = 10;
    const result = comptime fibonacci(10);
    std.debug.print("fibonacci(10): {d}\n", .{result});

    const divRes = divmod(100, 3);
    std.debug.print("100 / 3 = {d}, remainder = {d}\n", .{ divRes.quotient, divRes.remainder });

    // if は Rust 同様式としても使える。
    const ifExpress = if (divRes.quotient > 10) "big" else "small";
    std.debug.print("if express: {s}\n", .{ifExpress});

    const iterItems = [_]i32{ 1, 2, 3, 4, 5 };
    for (iterItems) |item| {
        std.debug.print("item: {d}\n", .{item});
    }

    for (0..3) |i| {
        std.debug.print("range item: {d}\n", .{i});
    }

    const divResult = try divide(10, 20);
    std.debug.print("divide result: {d}\n", .{divResult});

    processFile("data.txt") catch |err| {
        std.debug.print("failed to process file: {}\n", .{err});
    };

    const numbers = [_]i32{ 10, 20, 30, 40, 50 };
    // default with orelse
    const index1 = find(&numbers, 30) orelse 999;
    std.debug.print("index: {}\n", .{index1});

    const p1 = Point.init(3, 4);
    std.debug.print("point distance: {}\n", .{p1.distance()});
}

fn fibonacci(n: comptime_int) comptime_int {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fn add(x: i32, y: i32) i32 {
    return x + y;
}

const DivResult = struct {
    quotient: i32,
    remainder: i32,
};

fn divmod(a: i32, b: i32) DivResult {
    return DivResult{
        .quotient = @divTrunc(a, b),
        .remainder = @rem(a, b),
    };
}

/// Zig Pointers:
/// https://ziglang.org/documentation/0.15.2/#Pointers
fn increment(x: *i32) void {
    x.* += 1;
}

/// 計算時に発生しうるエラーセットの定義。
// Error-Set-Type: https://ziglang.org/documentation/0.15.2/#Error-Set-Type
const MathError = error{
    DivisionByZero,
    Overflow,
    NegativeValue,
};

// エラーユニオン, Result<T, E> 相当。
fn divide(a: i32, b: i32) MathError!i32 {
    // エラーは全てグローバル空間に登録される！！ほえええ
    // Error-Set-Type: https://ziglang.org/documentation/0.15.2/#Error-Set-Type
    if (b == 0) return error.DivisionByZero;
    return @divTrunc(a, b);
}

const FileError = error{ FileNotFound, PermissionDenied };

fn readFile(path: []const u8) FileError![]const u8 {
    if (std.mem.eql(u8, path, "not-found.txt")) {
        return error.FileNotFound;
    }
    return "file contents here";
}

// エラーユニオン演算子 "!" は (FileError | void) みたいな感じか？
fn processFile(path: []const u8) FileError!void {
    // try でエラーを伝播, Rust の "?" と同等。
    const contents = try readFile(path);
    std.debug.print("Contents: {s}\n", .{contents});
}

// Optional.
fn find(items: []const i32, target: i32) ?usize {
    for (items, 0..) |item, i| {
        if (item == target) return i;
    }
    return null;
}

const User = struct {
    name: []const u8,
    email: ?[]const u8,
};

fn getUserEmail(user: User) []const u8 {
    return user.email orelse "noemail";
}

const Point = struct {
    x: f32,
    y: f32,

    // default value のサポート。
    z: f32 = 0.0,

    pub fn init(x: f32, y: f32) Point {
        return Point{ .x = x, .y = y };
    }

    pub fn distance(self: Point) f32 {
        return @sqrt(self.x * self.x + self.y * self.y);
    }

    pub fn add(self: Point, other: Point) Point {
        return Point{
            .x = self.x + other.x,
            .y = self.y + other.y,
        };
    }
};

test "add" {
    const res = add(10, 20);
    try std.testing.expectEqual(30, res);
}

test "negative numbers" {
    const res = add(-10, -20);
    try std.testing.expectEqual(-30, res);
}
