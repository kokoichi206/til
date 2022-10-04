import Puppetter from "puppeteer";

import crawler, { Member } from './crawler';

async function main() {
  const browser = await Puppetter.launch(crawler.launchOptions());

  const members = await crawler.crawl(browser);
  browser.close();
}

main()
