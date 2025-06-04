import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

webdriver_path = "edgedriver_win64/msedgedriver.exe"
service = Service(webdriver_path)
options = Options()

driver = webdriver.Edge(service=service, options=options)

# urls = [
#    "https://www.thegioididong.com/may-doi-tra/laptop/acer-swit-5-sf514-53t-740r-i7-8565u-8gb-256gb-14f/detail?oldid=41615562&pid=208861&type=2",
#    "https://www.thegioididong.com/may-doi-tra/laptop/msi-gaming-leopard-gp76-11ug-i7-823vn/detail?oldid=40138398&pid=261962&type=2",
#     "https://www.thegioididong.com/may-doi-tra/laptop/apple-macbook-air-m2-2022/detail?oldid=43362327&pid=282827&type=2"
# ]

# Đọc file CSV chứa danh sách URLs
df = pd.read_csv('url_final.csv')

# Truy cập cột 'URL' trong DataFrame
urls = df['URL'].tolist()

def get_price(driver):
    price_new = None
    price_old = None
    try:
        # Tìm phần tử div có class "mPrice"
        price_element = driver.find_element(By.CSS_SELECTOR, "div.mPrice")

        # Tìm thẻ strong trong phần tử "mPrice" và lấy nội dung bên trong thẻ strong
        strong_element = price_element.find_element(By.CSS_SELECTOR, "strong")
        price_old = strong_element.text
        strong_element = price_element.find_element(By.CSS_SELECTOR, "span")
        price_new = strong_element.text
    except:
        return price_old, price_new

    return price_old, price_new
def get_warranty(driver):
    warranty = None

    try:
        li_element = driver.find_element(By.CSS_SELECTOR, 'li[data-v-70a9ac79]')
        bao_hanh_element = li_element.find_element(By.CSS_SELECTOR, "strong")
        warranty = bao_hanh_element.text
    except:
        return warranty

    return warranty

def get_name(driver):
    # Tìm tất cả các phần tử div với class "titleName"
    name = None
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "div.titleName")
        if name_element:
            # Nếu có phần tử, lấy nội dung của phần tử đầu tiên
            name = name_element.text
    except:
        return name
    return name
def scrape_data(driver):
    CPU = None
    Ram_size = None
    Ram_type = None
    Hard_Drive = None
    screen = None
    resolution = None
    graphics = None
    size_weight = None
    material = None
    os = None
    year = None
    battery = None

    try:
        wait = WebDriverWait(driver, 2)
        button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnViewFullSpec")))
        button.click()
        cpu_info_elements = driver.find_elements(By.XPATH,
                                                 "//div[contains(@class, 'speciTable speciFull')]//div[contains(text(), 'Bộ xử lý')]//following-sibling::table//td")
        ram_info_elements = driver.find_elements(By.XPATH,
                                                 "//div[contains(@class, 'speciTable speciFull')]//div[contains(text(), 'Bộ nhớ RAM, Ổ cứng')]//following-sibling::table//td")
        screen_info_elements = driver.find_elements(By.XPATH,
                                                    "//div[contains(@class, 'speciTable speciFull')]//div[contains(text(), 'Màn hình')]//following-sibling::table//td")
        graphics_info_elements = driver.find_elements(By.XPATH,
                                                      "//div[contains(@class, 'speciTable speciFull')]//div[contains(text(), 'Đồ họa và Âm thanh')]//following-sibling::table//td")
        size_weight_info_elements = driver.find_elements(By.XPATH,
                                                         "//div[contains(@class, 'speciTable speciFull')]//div[contains(text(), 'Kích thước & khối lượng')]//following-sibling::table//td")
        other_info_elements = driver.find_elements(By.XPATH,
                                                   "//div[contains(@class, 'speciTable speciFull')]//div[contains(text(), 'Thông tin khác')]//following-sibling::table//td")

        # Lấy thông tin từ các thẻ và in ra
        for index, element in enumerate(cpu_info_elements):
            if element.text == 'Công nghệ CPU':
                if index + 1 < len(cpu_info_elements):
                    CPU = cpu_info_elements[index + 1].text
                break

        for index, element in enumerate(ram_info_elements):
            if element.text == 'RAM':
                if index + 1 < len(ram_info_elements):
                    Ram_size = ram_info_elements[index + 1].text
            if element.text == 'Loại RAM':
                if index + 1 < len(ram_info_elements):
                    Ram_type = ram_info_elements[index + 1].text
            if element.text == 'Ổ cứng':
                if index + 1 < len(ram_info_elements):
                    Hard_Drive = ram_info_elements[index + 1].text

        for index, element in enumerate(screen_info_elements):
            if element.text == 'Màn hình':
                if index + 1 < len(screen_info_elements):
                    screen = screen_info_elements[index + 1].text
            if element.text == 'Độ phân giải':
                if index + 1 < len(screen_info_elements):
                    resolution = screen_info_elements[index + 1].text

        for index, element in enumerate(graphics_info_elements):
            if element.text == 'Card màn hình':
                if index + 1 < len(graphics_info_elements):
                    graphics = graphics_info_elements[index + 1].text

        for index, element in enumerate(size_weight_info_elements):
            if element.text == 'Kích thước, khối lượng':
                if index + 1 < len(size_weight_info_elements):
                    size_weight = size_weight_info_elements[index + 1].text

            if element.text == 'Chất liệu':
                if index + 1 < len(size_weight_info_elements):
                    material = size_weight_info_elements[index + 1].text

        for index, element in enumerate(other_info_elements):
            if element.text == 'Hệ điều hành':
                if index + 1 < len(other_info_elements):
                    os = other_info_elements[index + 1].text

            if element.text == 'Thời điểm ra mắt':
                if index + 1 < len(other_info_elements):
                    year = other_info_elements[index + 1].text

            if element.text == 'Thông tin Pin':
                if index + 1 < len(other_info_elements):
                    battery = other_info_elements[index + 1].text
    except:
        return CPU, Ram_size, Ram_type, Hard_Drive, screen, resolution, graphics, size_weight, material, os, year, battery
    return CPU, Ram_size, Ram_type, Hard_Drive, screen, resolution, graphics, size_weight, material, os, year, battery

data = []
i = 0
start_time = time.time()
for url in urls[:20]:
    i = i + 1
    print(i, "/1125")
    driver.get(url)
    name = get_name(driver)
    price_old, price_new = get_price(driver)
    warranty = get_warranty(driver)
    CPU, Ram_size, Ram_type, Hard_Drive, screen, resolution, graphics, size_weight, material, os, year, battery = scrape_data(driver)

    data.append({'name': name, 'price_old': price_old, 'price_new': price_new,'warranty': warranty, 'CPU': CPU, 'Ram_size': Ram_size,
                 'Ram_type': Ram_type, 'Hard_Drive': Hard_Drive, 'screen': screen, 'resolution': resolution, 'graphics': graphics,
                 'size_weight': size_weight, 'material': material, 'os': os, 'year':year, 'battery': battery})

driver.quit()
end_time = time.time()
print("Thời gian crawl: ", end_time - start_time, "s")

df = pd.DataFrame(data)

df.to_csv('data.csv', index=False)