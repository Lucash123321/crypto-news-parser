import asyncio
import datetime
from arsenic import get_session, services
from arsenic.browsers import Chrome


async def main():
    tasks = [asyncio.create_task(parse_data(datetime.datetime.now() + datetime.timedelta(0, i))) for i in range(10)]
    await asyncio.gather(*tasks)


async def parse_data(start_time):
    while datetime.datetime.now() < start_time:
        await asyncio.sleep(0.1)

    service = services.Chromedriver(binary=".\chromedriver.exe")
    options = {"goog:chromeOptions": {'args': ['--disable-gpu', '-–disk-cache-size=0'], }}
    async with get_session(service, Chrome(**options)) as session:

        async def session_loop(start_time):

            while datetime.datetime.now() < start_time:
                await asyncio.sleep(0.1)

            await session.get('https://announcements.bybit.com/en-US/?category=&page=1')

            selector = """
            #__next > div > main > div.announcement-contentstack-layout > 
            div > div.ant-row.page-article-content.light > 
            div.ant-col.ant-col-24.page-article-content-announcement.ant-col-lg-18 > 
            div > a:nth-child(1)
            """

            try:
                new_data = await session.wait_for_element(selector=selector, timeout=10)
                new_data_text = await new_data.get_text()
                new_data_text = new_data_text.split("\n")
                url = await new_data.get_attribute("href")
                url = 'https://announcements.bybit.com' + url
                if new_data_text[0] == "Top":
                    title = new_data_text[1]
                else:
                    title = new_data_text[0]

                data.append(str(start_time))
                data.append(title)
                data.append(url)
                data.append("\n")
                if title not in unique_titles:
                    with open('output.csv', 'a', newline='') as csv_file:
                        csv_file.write(' '.join(data))
                    unique_titles.add(title)
                data.clear()

            except TimeoutError:
                pass

        while True:
            await session_loop(start_time)
            start_time = start_time + datetime.timedelta(0, 10)

unique_titles = set()
data = []
begin = datetime.datetime.now()

if __name__ == '__main__':
    asyncio.run(main())
