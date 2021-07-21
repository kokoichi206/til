from notion_api import NotionAPI
from drive import FetchPdfNames


def main():
    fetcher = FetchPdfNames()
    notion_user = NotionAPI()
    
    pdf_infos = fetcher.get_new_pdf_infos_since("2021/07/08")
    for pdf_info in pdf_infos:
        print(pdf_info)
        notion_user.post_pdf(pdf_info)


if __name__ == "__main__":
    main()
