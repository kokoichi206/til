const rl = @import("raylib");

pub fn main() void {
    const screenWidth = 800;
    const screenHeight = 600;

    rl.initWindow(screenWidth, screenHeight, "Zig Invaders");
    defer rl.closeWindow();

    rl.setTargetFPS(60);

    while (!rl.windowShouldClose()) {
        rl.beginDrawing();
        // zig の defer はここで閉じる。
        defer rl.endDrawing();

        rl.clearBackground(rl.Color.black);
        rl.drawText("Zig invaders", 300, 250, 40, rl.Color.green);
    }
}
