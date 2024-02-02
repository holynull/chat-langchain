import asyncio
from pyppeteer import launch

async def fetch_page(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    html_content = await page.content()
    await browser.close()
    return html_content

url = "https://www.globenewswire.com/news-release/2024/02/02/2822571/0/en/Crispmind-Set-to-Revolutionize-Cryptocurrency-Spending-with-Tectum-Emission-Token-Listing-on-Travala.html"

# 获取页面内容
html_content = asyncio.get_event_loop().run_until_complete(fetch_page(url))

# 打印页面内容
print(html_content)