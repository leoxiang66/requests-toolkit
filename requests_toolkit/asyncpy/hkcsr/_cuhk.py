import aiohttp
import asyncio
from bs4 import BeautifulSoup

base_url = "https://www.cse.cuhk.edu.hk/people/faculty/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


async def fetch(session, url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers,ssl=False) as response:
                return await response.text()
        except aiohttp.ClientConnectorError as e:
            print(f"Attempt {attempt + 1} to fetch {url} failed with error: {e}")
            await asyncio.sleep(2)  # 等待一段时间后重试
    print(f"Failed to fetch {url} after {retries} attempts")
    return None


async def get_teacher_links(session, base_url):
    html = await fetch(session, base_url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        # 找到所有 class 为 'sptp-member-avatar' 的 <a> 标签的链接
        teacher_links = [
            a["href"]
            for a in soup.find_all("a", href=True, class_="sptp-member-avatar")
        ]
        return teacher_links
    return []


async def get_email_and_interests_from_teacher_page(session, url):
    html = await fetch(session, url)
    if html:
        soup = BeautifulSoup(html, "html.parser")

        # 提取电子邮件
        email_tag = soup.find("i", class_="fas fa-envelope")
        if email_tag:
            email = email_tag.find_next("span")
            if email:
                email = email.text
        else:
            email = None
        # 提取研究兴趣
        interests = []
        research_areas_section = soup.find('strong', text='Research Areas')
        if research_areas_section:
            next_div = research_areas_section.find_next('div')
            if next_div:
                interest_list = next_div.find_all('li')
                for item in interest_list:
                    interests.append(item.get_text(strip=True))

        return email, interests
    return None, None


async def CUHK():
    async with aiohttp.ClientSession() as session:
        teacher_links = await get_teacher_links(session, base_url)
        teacher_info = {}

        tasks = []
        for link in teacher_links:
            full_url = link if link.startswith("http") else base_url + link[16:]
            tasks.append(get_email_and_interests_from_teacher_page(session, full_url))

        results = await asyncio.gather(*tasks)

        for link, (email, interests) in zip(teacher_links, results):
            if email or interests:
                full_url = link if link.startswith("http") else base_url + link[16:]
                teacher_info[full_url] = {"email": email, "interests": interests}

        return teacher_info


if __name__ == "__main__":
    asyncio.run(CUHK())