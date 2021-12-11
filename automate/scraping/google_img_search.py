import sys
import argparse
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler


def scrapingImages(name: str, dir_name: str, max_num: int):
    google_crawler = GoogleImageCrawler(storage={'root_dir': f'./imgs/{dir_name}'})
    google_crawler.crawl(keyword=f'{name}', max_num=max_num)
    yahoo_crawler = BingImageCrawler(storage={'root_dir': f'./imgs_bing/{dir_name}'})
    yahoo_crawler.crawl(keyword=f'{name}', max_num=max_num)

def parseArgs() -> list:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', '--name', type=str,
                        help='sum the integers (default: find the max)',
                        default="藤吉夏鈴")
    parser.add_argument('-nr', '--name-roman', type=str,
                        help='sum the integers (default: find the max)',
                        default="fujiyoshikarin")
    parser.add_argument('--max-num', type=int,
                        help='sum the integers (default: find the max)',
                        default=100)
    args = parser.parse_args()
    return args

def isValidName(name: str, nameEn: str) -> bool:
    return not ((name == '藤吉夏鈴') ^ (nameEn == 'fujiyoshikarin'))


if __name__ == '__main__':
    args = parseArgs()
    if not isValidName(args.name, args.name_roman):
        sys.exit("Name or Name-Roman is Invalid")
    scrapingImages(name=args.name, dir_name=args.name_roman, max_num=args.max_num)
