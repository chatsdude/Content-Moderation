from newspaper import Article

class ArticleScraper:
    def __init__(self,urlParam):
        self.articleObj = Article(urlParam)

    
    def scrapeArticle(self):
        try:
            self.articleObj.download()
            self.articleObj.parse()
            title = self.articleObj.title
            content = self.articleObj.text
            return title + content
        except Exception as e:
            print(e)
