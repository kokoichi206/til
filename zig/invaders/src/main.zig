const rl = @import("raylib");

const Rectangle = struct {
    x: f32,
    y: f32,
    width: f32,
    height: f32,

    pub fn intersects(self: Rectangle, other: Rectangle) bool {
        return self.x < other.x + other.width and
            self.x + self.width > other.x and
            self.y < other.y + other.height and
            self.y + self.height > other.y;
    }
};

const GameConfig = struct {
    screenWidth: i32,
    screenHeight: i32,
    playerWidth: f32,
    playerHeight: f32,
    playerStartY: f32,
    bulletWidth: f32,
    bulletHeight: f32,
    shieldStartX: f32,
    shieldY: f32,
    shieldWidth: f32,
    shieldHeight: f32,
    shieldSpacing: f32,
    invaderStartX: f32,
    invaderStartY: f32,
    invaderWidth: f32,
    invaderHeight: f32,
    invaderSpacingX: f32,
    invaderSpacingY: f32,
};

// const Example = struct {
//     value: i32,

//     pub fn init(starting_value: i32) @This() {
//         return .{
//             .value = starting_value,
//         };
//     }

//     // to modify data, use pointer with *.
//     pub fn update(self: *@This()) void {
//         self.value += 1;
//     }
// };

const Player = struct {
    position_x: f32,
    position_y: f32,
    width: f32,
    height: f32,
    speed: f32,

    pub fn init(
        pos_x: f32,
        pos_y: f32,
        width: f32,
        height: f32,
    ) @This() {
        return .{
            .position_x = pos_x,
            .position_y = pos_y,
            .width = width,
            .height = height,
            .speed = 5.0,
        };
    }
};

pub fn main() void {
    const screenWidth = 800;
    const screenHeight = 600;

    rl.initWindow(screenWidth, screenHeight, "Zig Invaders");
    defer rl.closeWindow();

    const playerWidth = 50.0;
    const playerHeight = 30.0;
    
    var player = Player.init(
        @as(f32, @floatFromInt(screenWidth)) / 2 - playerWidth / 2,
        @as(f32, @floatFromInt(screenHeight)) - 60.0,
        playerWidth,
        playerHeight,
    );

    rl.setTargetFPS(60);

    while (!rl.windowShouldClose()) {
        rl.beginDrawing();
        // zig の defer はここで閉じる。
        defer rl.endDrawing();

        rl.clearBackground(rl.Color.black);
        rl.drawText("Zig invaders", 300, 250, 40, rl.Color.green);
    }
}
