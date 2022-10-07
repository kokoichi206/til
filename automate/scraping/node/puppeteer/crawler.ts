import puppeteer from 'puppeteer';

export interface Member {
  name: string;
  birthday: string;
  bloodType: string;
  constellation: string;
  height: string;
  sns?: string;
}
export function memberToFileContent(member: Member): string {
  const base = `名前: ${member.name}\n生年月日: ${member.birthday}` + 
              `\n血液型: ${member.bloodType}\n星座: ${member.constellation}\n身長: ${member.height}\n`;
  if (member.sns) return base + `SNS: ${member.sns}\n`;
  return base;
}

export default {
  url: "https://www.nogizaka46.com/s/n46/search/artist?ima=0606",

  launchOptions: (headless = true) => {
    return {
      headless: headless,
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
  },

  async crawl(browser: puppeteer.Browser): Promise<Member[]> {
    const page = await browser.newPage();

    await page.goto(this.url);
    await this.setupPage(page);

    const links = await this.fetchLinks(page);
    console.log(`${links.length} links found.`);
    console.log(links);

    const members = await this.fetchMembers(page, links);
    console.log("========== Members info ==========");
    console.log(members);

    return members;
  },

  setupPage: async function(page: puppeteer.Page) {
    // set language
    await page.setExtraHTTPHeaders({
      "Accept-Language": "ja-JP"
    });

    // no cache
    await page.setCacheEnabled(false);
  },

  fetchLinks: async function (page: puppeteer.Page): Promise<string[]> {
    const navSelector = "a.m--mem__in";
    return await page.$$eval(navSelector, el => {
      return el
        .map(e => (e as HTMLAnchorElement).href)
    })
  },

  fetchMembers: async function (page: puppeteer.Page, urls: string[]): Promise<Member[]> {
    
    const members: Member[] = [];

    for (const url of urls) {
      const member = await this.fetchMember(page, url);
      if (member) {
        members.push(member);
      } else {
        // member is null.
        console.error(`Unexpected error happened: url ${url}`);
        // process.exit(1);
      }
    }
    return members;
  },

  fetchMember: async function (page: puppeteer.Page, url: string): Promise<Member|null> {

    const retry = 3;
    const contentSelector = ".md--hd__in";

    for (let i = 0; i < retry; i++) {
      try {
        await page.goto(url);
        await page.waitForSelector(contentSelector);

        const name = await page.$eval("h1.md--hd__ttl", el => el.textContent!.trim());
        const infos = await page.$$eval("dd.md--hd__data__d", el => {
          return el.map(e => e.textContent!)
        });

        if (infos.length >= 4) {
          let member: Member = {
            name: name,
            birthday: infos[0],
            bloodType: infos[1],
            constellation: infos[2],
            height: infos[3],
          }
          // 人によっては SNS アカウント情報がある。
          if (infos.length == 5) member.sns = infos[4];
          return member;  
        }
      } finally {
        console.log(`Retried counts ${i + 1}`)
      }
    }

    return null;
  }
}
