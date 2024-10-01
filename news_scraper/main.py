"""For scraping a url for useful links"""
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_html(url):
    """Get the html string from url"""
    with urlopen(url) as page:
        html_bytes = page.read()
        html = html_bytes.decode("utf_8")
    return html


def parse_stories_bs(domain_url, scrape_url, html):
    """Generate a list of stories from a html string."""
    stories = []
    soup = BeautifulSoup(html, "html.parser")
    article_list = []
    a_tag_list = soup.css.select("a")
    for tag in a_tag_list:
        if domain_url == scrape_url:
            if "excerpt-content" in tag.get("class"):
                article_list.append(tag)
        elif tag.get("class") and "ssrcss-18cjaf3-Headline" in tag.get("class"):
            article_list.append(tag)

    title_list = []
    for article in article_list:
        title = article.get_text("h3").split('h3')[-1]
        url = article.get("href")
        if "http" not in url:
            url = domain_url + url
        if url[8:12] == "www.":
            url = url[:8] + url[12:]
        if title not in title_list:
            title_list.append(title)
            stories.append({"title": title,
                            "url": url})
    return stories


def space_articles(input_url):
    """Return a list of url and title scraped from a webpage."""
    html_doc = get_html(input_url)
    return parse_stories_bs(input_url, input_url, html_doc)


if __name__ == "__main__":
    BBC_URL = "https://bbc.co.uk"
    SPACE_URL = "https://www.ukspace.org/news/"
    print(get_html(SPACE_URL))
    print(space_articles(SPACE_URL))
