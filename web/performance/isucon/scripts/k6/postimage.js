import http from "k6/http";

import { parseHTML } from "k6/html";

import { url } from "./config.js";

// open as binary file.
const testImage = open("aya.png", "b");

export default function () {
  const login_response = http.post(url("/login"), {
    account_name: "hoge",
    password: "hogehoge",
  });
  const doc = parseHTML(login_response.body);
  const token = doc.find('input[name="csrf_token"]').first().attr("value");

  http.post(url("/"), {
    file: http.file(testImage, "testimage.png", "image/png"),
    body: "Posted by k6",
    csrf_token: token,
  });
}
