import Puppetter from "puppeteer";

const launchOptions = {
  headless: true,
  slowMo: 100,
  defaultViewport: {
    width: 1700,
    height: 1000
  },
  args: [
    '--lang=ja',
    '--no-sandbox'
  ],
}

async function main() {
  const browser = await Puppetter.launch(launchOptions);
  const url = "https://pptr.dev/";

  const page = await browser.newPage();
  await setupPage(page);
  await page.goto(url);

  const selector = ".anchor";
  const links = await page.$$eval(selector, el => {
    return el.map(e => e.textContent);
  });
  console.log(links);
  browser.close();
}

async function setupPage(page: Puppetter.Page): Promise<void> {
  await page.setExtraHTTPHeaders({
    "Accept-Language": "ja-JP"
  });

  await page.setCacheEnabled(false);
}

main()
