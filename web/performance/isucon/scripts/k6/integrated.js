import initialize from "./initialize";
import comment from "./comment";
import postimage from "./postimage";

// k6 が各函数を実行できるように
export { initialize, comment, postimage };

export const options = {
  scenarios: {
    initialize: {
      executor: "shared-iterations",
      vus: 1,
      iterations: 1,
      // 実行シナリオの関数名。
      exec: "initialize",
      maxDuration: "10s",
    },
    comment: {
      // 複数の VUs を並行で動かす実行機構。
      executor: "constant-vus",
      vus: 4,
      duration: "30s",
      exec: "comment",
      startTime: "12s",
    },
    postImage: {
      executor: "constant-vus",
      vus: 2,
      duration: "30s",
      exec: "postimage",
      startTime: "12s",
    },
  },
};

export default function () {}
