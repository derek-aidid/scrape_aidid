from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

def n591(url):
    print(f"Visiting URL: {url}")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver2 = webdriver.Chrome(options=chrome_options)
    results = []
    try:
        driver.get(url)
        time.sleep(3)  # wait for elements to load

        urls = [element.get_attribute('href') for element in driver.find_elements(By.XPATH, '//div[@class="houseList-item-title"]/a')]
        print(urls)
        urls = [url for url in urls if url != 'javascript:void(0);']
        for link in urls:
            print(f"Visiting link: {link}")
            driver2.get(link)
            time.sleep(4) # wait for elements to load

            # get data
            try:
                name = driver2.find_element(By.XPATH, '//h1[@class="detail-title-content"]').text
            except Exception as e:
                continue

            try:
                price = driver2.find_element(By.XPATH, '//div[@class="info-price-left"]').text.strip()
            except Exception as e:
                price = None


            try:
                layout = driver2.find_element(By.XPATH, ".//div[@class='info-floor-key' and text()[contains(., '房')]]").text
            except Exception as e:
                layout = None

            try:
                house_type = driver2.find_element(By.XPATH, ".//div[@class='info-floor-key' and text()[contains(., '年')]]").text
            except Exception as e:
                house_type = None

            try:
                space = driver2.find_element(By.XPATH, ".//div[@class='info-floor-key' and text()[contains(., '坪')]]").text
            except Exception as e:
                space = None

            try:
                floors = driver2.find_element(By.XPATH, ".//div[@class='info-addr-content']/span[contains(text(), '樓')]/following-sibling::span").text
            except:
                floors = '無'

            try:
                community = driver2.find_element(By.XPATH, ".//div[@class='info-addr-content']/span[contains(text(), '社')]/following-sibling::span").text
            except:
                community = '無'

            try:
                address = driver2.find_element(By.XPATH, ".//div[@class='info-addr-content']/span[contains(text(), '地')]/following-sibling::span").text
            except:
                address = '無'

            # Initialize the lists to store basic info and features
            basic_info = []
            features = []

            # Find all detail-house-box sections
            detail_house_boxes = driver2.find_elements(By.CLASS_NAME, 'detail-house-box')

            for box in detail_house_boxes:
                items = box.find_elements(By.CLASS_NAME, 'detail-house-item')
                for item in items:
                    try:
                        key = item.find_element(By.CLASS_NAME, 'detail-house-key').text
                        value = item.find_element(By.CLASS_NAME, 'detail-house-value').text
                        basic_info.append(f'{key}: {value}')
                    except:
                        try:
                            feature = item.find_element(By.CLASS_NAME, 'detail-house-value').text
                            features.append(feature)
                        except:
                            continue
                # Extract features from detail-house-life elements
                life_items = box.find_elements(By.CLASS_NAME, 'detail-house-life')
                for life_item in life_items:
                    try:
                        feature = life_item.text
                        features.append(feature)
                    except:
                        continue

            try:
                review_element = driver2.find_element(By.ID, 'detail-feature-text')
                review = review_element.text.strip().replace('\n', '')
                if not review:
                    review = '無'
            except:
                review = '無'

            try:
                direction = driver2.find_element(By.XPATH, ".//div[@class='info-addr-content']/span[contains(text(), '朝')]/following-sibling::span").text
                basic_info.append(f'朝向: {direction}')
            except:
                basic_info.append('朝向: 無')

            # Extract images
            images = []
            try:
                img_list_element = driver2.find_element(By.ID, 'img_list')
                img_elements = img_list_element.find_elements(By.TAG_NAME, 'img')
                for img in img_elements:
                    src = img.get_attribute('src')
                    images.append(src)
            except:
                images = []

            # Extract community history
            community_history = []
            try:
                community_info_element = driver2.find_element(By.CLASS_NAME, 'community-info-onsale-list')
                onsale_list_items = community_info_element.find_elements(By.CLASS_NAME, 'onsale-list-item')
                for item in onsale_list_items:
                    try:
                        spans = item.find_elements(By.TAG_NAME, 'span')
                        history_text = ' | '.join([span.text for span in spans])
                        community_history.append(history_text)
                    except Exception as e:
                        print(f"no history")
            except Exception as e:
                print(f"no history")

            result = {
                'url': link,
                'name': name,
                'address': address,
                'price': price,
                'layout': layout,
                'space': space,
                'house_type': house_type,
                'floor': floors,
                'community': community,
                'basic_info': basic_info,
                'features': features,
                'review': review,
                'images': images,
                'community_history': community_history,
            }

            print(result)
            results.append(result)
            with open('buy591.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')

    except Exception as e:
        print(f"Error visiting URL: {url}")


    driver.quit()
    driver2.quit()

    return results

if __name__ == "__main__":
    city0 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=1&firstRow={i}&totalRows=23364" for i in range(0, 23364, 30)]
    city1 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=3&firstRow={i}&totalRows=53465" for i in range(0, 53465, 30)]
    city2 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=6&totalRows=37657&firstRow={i}" for i in range(0, 37657, 30)]
    city3 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=4&totalRows=7127&firstRow={i}" for i in range(0, 7127, 30)]
    city4 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=5&totalRows=9371&firstRow={i}" for i in range(0, 9371, 30)]
    city5 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=21&totalRows=4541&firstRow={i}" for i in range(0, 4541, 30)]
    city6 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=2&totalRows=5050&firstRow={i}" for i in range(0, 5050, 30)]
    city7 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=8&totalRows=75566&firstRow={i}" for i in range(0, 75566, 30)]
    city8 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=10&totalRows=2857&firstRow={i}" for i in range(0, 2857, 30)]
    city9 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=14&totalRows=543&firstRow={i}" for i in range(0, 543, 30)]
    city10 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=7&totalRows=3066&firstRow={i}" for i in range(0, 3066, 30)]
    city11 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=11&totalRows=968&firstRow={i}" for i in range(0, 968, 30)]
    city12 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=17&totalRows=24454&firstRow={i}" for i in range(0, 24454, 30)]
    city13 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=15&totalRows=11392&firstRow={i}" for i in range(0, 11392, 30)]
    city14 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=12&totalRows=1015&firstRow={i}" for i in range(0, 1015, 30)]
    city15 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=13&totalRows=491&firstRow={i}" for i in range(0, 491, 30)]
    city16 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=19&totalRows=1879&firstRow={i}" for i in range(0, 1879, 30)]
    city17 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=22&totalRows=122&firstRow={i}" for i in range(0, 122, 30)]
    city18 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=23&totalRows=2149&firstRow={i}" for i in range(0, 2149, 30)]
    city19 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=24&totalRows=32&firstRow={i}" for i in range(0, 32, 30)]
    city20 = [f"https://sale.591.com.tw/?category=1&shType=list&regionid=25&totalRows=84&firstRow={i}" for i in range(0, 84, 30)]

    start_urls = city0 + city1 + city2 + city3 + city4 + city5 + city6 + city7 + city8 + city9 + city10 + city11 + city12 + city13 + city14 + city15 + city16 + city17 + city18 + city19 + city20
    # start_urls = city0 + city1 + city2
    start_urls = list(set(start_urls))
    futures = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in start_urls:
            futures.append(executor.submit(n591, url))

        for i, future in enumerate(as_completed(futures)):
            print(i)
            future.result()  # wait for all futures to complete

    print("Scraping completed.")

