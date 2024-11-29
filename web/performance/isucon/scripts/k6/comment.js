import http from "k6/http";

import { check } from "k6";

import { parseHTML } from "k6/html";

import { url } from "./config.js";

export default function () {
  const login_response = http.post(url("/login"), {
    account_name: "hoge",
    password: "hogehoge",
  });
  console.log("r.status: ", login_response.status);
  check(login_response, {
    "is status 200": (r) => r.status === 200,
  });

  // ユーザーページの取得。
  // Go 実装では `/` にアクセスが必要だった
  const res = http.get(url("/"));
  // const res = http.get(url("/@hoge"))
  console.log("res.status: ", res.status);
  console.log("res.body: ", res.body);
  const doc = parseHTML(res.body);

  // フォームの hidden 要素から抽出。
  const token = doc.find('input[name="csrf_token"]').first().attr("value");
  console.log("token: ", token);
  const post_id = doc.find('input[name="post_id"]').first().attr("value");
  console.log("post_id: ", post_id);

  const comment_res = http.post(url("/comment"), {
    post_id: post_id,
    csrf_token: token,
    comment: "Hello from k6",
    submit: "submit",
  });
  console.log("comment_res.status: ", comment_res.status);
  check(comment_res, {
    "is status 200": (r) => r.status === 200,
  });
}
