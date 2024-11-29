// see:
// https://grafana.com/docs/k6/latest/javascript-api/k6-data/sharedarray/
import { SharedArray } from "k6/data";

const accounts = new SharedArray("accounts", function () {
  return JSON.parse(open("./accounts.json"));
});

export function getAccount() {
  return accounts[Math.floor(Math.random() * accounts.length)];
}
