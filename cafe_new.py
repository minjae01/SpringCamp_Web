import time
import os
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 유튜브 링크 딕셔너리
link_dict = {
    "double dumbbell front rack lunge": "https://www.youtube.com/watch?v=7EmwtpAI8cM",
    "dumbbell shoulder to overhead": "https://www.youtube.com/watch?v=AQ50ji32egc",
    "high hang pause power snatch": "https://www.youtube.com/watch?v=JRMGMfRe8zY",
    "lateral burpee bar hop over": "https://www.youtube.com/watch?v=przJ5ZW-YSU",
    "burpee over the dumbbell": "https://www.youtube.com/watch?v=ZxFVFxMn6GY",
    "dumbbell hang clean & jerk": "https://www.youtube.com/watch?v=hTtXNkoqHyY",
    "burpee box jump over": "https://www.youtube.com/watch?v=GLktGkmcvWE",
    "front rack reverse lunge": "https://www.youtube.com/watch?v=LRYH5QlCa0o",
    "front rack lunge": "https://www.youtube.com/watch?v=f3WLs_HutLw",
    "double db snatch": "https://www.youtube.com/watch?v=-px4XoSZr1g",
    "burpee box get over": "https://www.youtube.com/watch?v=IvpYHAh-g48",
    "dumbbell hang cluster": "https://www.youtube.com/watch?v=N3KpHHv9jDo",
    "overhead dumbbell lunge": "https://www.youtube.com/watch?v=c-4dfhO8QTw",
    "wall ball shot": "https://www.youtube.com/watch?v=EqjGKsiIMCE",
    "bar muscle up": "https://www.youtube.com/watch?v=OCg3UXgzftc",
    "kettle bell swing": "https://www.youtube.com/watch?v=mKDIuUbH94Q",
    "dumbbell thruster": "https://www.youtube.com/watch?v=u3wKkZjE8QM",
    "sandbag squat": "https://www.youtube.com/watch?v=qcCuCcV78X8",
    "sandbag carry": "https://www.youtube.com/watch?v=DZtrqfa7Whg",
    "hand stand push up": "https://www.youtube.com/watch?v=qbRbM6d5ddM",
    "dumbbell snatch": "https://www.youtube.com/watch?v=-px4XoSZr1g",
    "power snatch": "https://www.youtube.com/watch?v=TL8SMp7RdXQ",
    "hang power snatch": "https://www.youtube.com/watch?v=z1j2QMBJF6c",
    "hang squat clean": "https://www.youtube.com/watch?v=YZUdVyVV3uI",
    "hang power clean": "https://www.youtube.com/watch?v=0aP3tgKZcHQ",
    "overhead squat": "https://www.youtube.com/watch?v=pn8mqlG0nkE",
    "rope climb": "https://www.youtube.com/watch?v=Pa4QUC9AvuA",
    "ring muscle up": "https://www.youtube.com/watch?v=G8W0BhzrWcs",
    "ab mat sit up": "https://www.youtube.com/watch?v=_HDZODOx7Zw",
    "shuttle run": "https://www.youtube.com/watch?v=3-iZMS6twcE",
    "calorie row": "https://www.youtube.com/watch?v=fxfhQMbATCw",
    "toes to bar": "https://www.youtube.com/watch?v=_03pCKOv4l4",
    "box jump over": "https://www.youtube.com/watch?v=f6AR27I-DwU",
    "power clean": "https://www.youtube.com/watch?v=KwYJTpQ_x5A",
    "pull up": "https://www.youtube.com/watch?v=aAggnpPyR6E",
    "deadlift": "https://www.youtube.com/watch?v=1ZXobu7JvvE",
    "wall walk": "https://www.youtube.com/watch?v=2TnX8j29tRY",
    "hang clean": "https://www.youtube.com/watch?v=DaKC_BEN5bk",
    "air squat": "https://www.youtube.com/watch?v=i8oGQ03wqZc",
    "front squat": "https://www.youtube.com/watch?v=uYumuL_G_V0",
    "thrusters": "https://www.youtube.com/watch?v=L219ltL15zk",
    "burpee pull up": "https://www.youtube.com/watch?v=qCldcUyNyPE",
    "burpee": "https://www.youtube.com/watch?v=auBLPXO8Fww",
    "cal row": "https://www.youtube.com/watch?v=fxfhQMbATCw",
    "cal machine": "https://www.youtube.com/watch?v=fxfhQMbATCw",
    "farmer's carry": "https://www.youtube.com/watch?v=p5MNNosenJc",
    "overhead lunge": "https://www.youtube.com/watch?v=c-4dfhO8QTw",
    "bar facing burpee": "https://www.youtube.com/watch?v=A6gQLuMMiA4",
    "squat clean": "https://www.youtube.com/watch?v=YZUdVyVV3uI",
    "burpee over the bar": "https://www.youtube.com/watch?v=D7rAEEE_H9A"
}

def auto_link(text: str, word_links: dict) -> str:
    sorted_words = sorted(word_links.keys(), key=lambda w: -len(w))
    matches = []

    for word in sorted_words:
        url = word_links[word]
        pattern = re.compile(re.escape(word), flags=re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.start(), match.end()
            if any(s < end and start < e for s, e, _ in matches):
                continue
            matches.append((start, end, url))

    matches.sort(reverse=True)
    for start, end, url in matches:
        matched_text = text[start:end]
        anchor = f'<a href="{url}" target="_blank">{matched_text}</a>'
        text = text[:start] + anchor + text[end:]
    return text

# 📅 월~금 날짜 리스트 생성
today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
weekday_dates = [monday + datetime.timedelta(days=i) for i in range(5)]

all_html_blocks = []

for target_date in weekday_dates:
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\\Temp\\SeleniumTestProfile")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print(f"🚀 {target_date} 크롬 실행 중...")

    cafe_url = "https://cafe.naver.com/f-e/cafes/31082758/menus/2?viewType=L"
    driver.get(cafe_url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    posts = driver.find_elements(By.CSS_SELECTOR, "a.article")
    wod_posts = [post for post in posts if "WOD" in post.text]

    if not wod_posts:
        print("❗ WOD 게시글을 찾을 수 없습니다.")
        driver.quit()
        continue

    latest_post = wod_posts[0]
    href = latest_post.get_attribute("href")
    full_link = f"https://cafe.naver.com{href}" if href.startswith("/") else href

    driver.get(full_link)
    time.sleep(3)

    try:
        driver.switch_to.frame("cafe_main")
    except:
        pass

    try:
        content_element = driver.find_element(By.CSS_SELECTOR, '.se-main-container')
        content_text = content_element.text
    except:
        try:
            content_element = driver.find_element(By.CSS_SELECTOR, '.ContentRenderer')
            content_text = content_element.text
        except:
            content_text = "(본문을 불러올 수 없습니다.)"

    today_str = target_date.strftime("%Y년 %#m월 %#d일") if os.name == 'nt' else target_date.strftime("%Y년 %-m월 %-d일")
    lines = content_text.splitlines()
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if today_str in line:
            start_idx = i

    for i in range(start_idx + 1, len(lines)):
        if "Beginner" in lines[i]:
            end_idx = i
            break

    if start_idx != -1 and end_idx != -1 and start_idx <= end_idx:
        filtered_lines = lines[start_idx:end_idx + 1]
        wod_text = "\n".join(filtered_lines)
    else:
        wod_text = f"❗ {today_str} 또는 'Beginner'를 찾을 수 없습니다."

    driver.quit()

    wod_text = auto_link(wod_text, link_dict)

    # ✅ 들여쓰기 없이 HTML 블록 저장
    date_header = f"<h2>{target_date.strftime('%Y-%m-%d')} ({target_date.strftime('%A')})</h2>"
    html_block = f"""\
{date_header}
<img src="/static/title.png" alt="Spring Camp Title" class="header-image" />
<div class="content">{wod_text.replace('\n', '<br>')}</div>
<hr>""".strip()

    all_html_blocks.append(html_block)
    print(f"✅ {target_date.strftime('%Y-%m-%d')} WOD 저장 완료")

# ✅ 최종 통합 저장
with open("wod_text.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_html_blocks))

print("🎉 전체 WOD가 wod_text.txt에 저장 완료되었습니다!")
