import Puppetter from "puppeteer";
import fs from "fs/promises";

import crawler, { Member, memberToFileContent } from './crawler';

async function saveMembers(members: Member[]) {
  const dirPath = "./docs/";
  await fs.stat(dirPath);
  await fs.rm(dirPath, { recursive: true, force: true });
  await fs.mkdir(dirPath);

  await Promise.all(members.map(async member => {
    const fileName = member.name.replace(/[\s]/g, "");
    const fullPath = `${dirPath}${fileName}.txt`
    await fs.writeFile(fullPath, memberToFileContent(member), "utf-8");
  }))
}

async function main() {
  const browser = await Puppetter.launch(crawler.launchOptions());

  const members = await crawler.crawl(browser);
  await saveMembers(members);
  browser.close();
}

main()
