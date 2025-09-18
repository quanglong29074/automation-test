#!/usr/bin/env python3
import os
import time
import logging
import base64
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

# ------------------ Load ENV ------------------
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# ------------------ Cấu hình ------------------
os.makedirs("screenshots", exist_ok=True)

logging.basicConfig(
    filename="report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log(msg: str):
    print(msg)
    logging.info(msg)


def capture_with_error(driver, screenshot_path: str, error_message: str):
    """Chụp màn hình khi fail"""
    try:
        driver.save_screenshot(screenshot_path)
        print(f"📸 Đã chụp màn hình: {screenshot_path}")
        print(f"❌ Lỗi: {error_message}")
    except Exception as e:
        print(f"⚠️ Không thể chụp màn hình: {e}")


def create_github_issue(title: str, body: str, screenshot_path: str = None):
    """Tạo issue trên GitHub kèm screenshot"""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        print("⚠️ Chưa cấu hình GITHUB_TOKEN hoặc GITHUB_REPO trong .env")
        return

    image_markdown = ""
    if screenshot_path and os.path.exists(screenshot_path):
        try:
            with open(screenshot_path, "rb") as f:
                content = base64.b64encode(f.read()).decode("utf-8")
            image_name = os.path.basename(screenshot_path)
            upload_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/screenshots/{image_name}"
            res = requests.put(
                upload_url,
                headers={"Authorization": f"token {GITHUB_TOKEN}"},
                json={
                    "message": f"upload screenshot {image_name}",
                    "content": content,
                },
            )
            if res.status_code in [200, 201]:
                download_url = res.json()["content"]["download_url"]
                image_markdown = f"\n\n![screenshot]({download_url})"
            else:
                print("⚠️ Upload ảnh thất bại:", res.text)
        except Exception as e:
            print("⚠️ Lỗi khi upload ảnh:", e)

    # Tạo issue
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    payload = {"title": title, "body": body + image_markdown}
    res = requests.post(
        url,
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
        json=payload,
    )
    if res.status_code == 201:
        issue_url = res.json()["html_url"]
        print(f"✅ Đã tạo GitHub Issue: {issue_url}")
    else:
        print("⚠️ Tạo issue thất bại:", res.text)


def run_testcase(file_path: str):
    """Chạy một file testcase"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1280, 800)
    driver.implicitly_wait(5)

    total, passed, failed = 0, 0, 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            steps = [s.strip() for s in f.readlines() if s.strip()]

        i = 0
        while i < len(steps):
            step = steps[i]
            total += 1
            log(f"➡️ Bước: {step}")

            try:
                # ------------------ Mở trang ------------------
                if step.startswith(("mở trang", "vào trang")):
                    url = step.split(" ", 2)[2].strip()
                    driver.get(url)

                # ------------------ Nhập text ------------------
                elif step.startswith("nhập text "):
                    if "vào ô" in step:
                        parts = step.split("vào ô")
                        text = parts[0].replace("nhập text", "").strip()
                        selector = parts[1].strip()
                        elem = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        elem.clear()
                        elem.send_keys(text)

                # ------------------ Nhập nhiều field ------------------
                elif step.startswith("nhập text nhiều"):
                    j = i + 1
                    while j < len(steps) and ":" in steps[j]:
                        field, value = steps[j].split(":", 1)
                        field, value = field.strip(), value.strip()
                        selector = f"input[name='{field}']"
                        elem = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        elem.clear()
                        elem.send_keys(value)
                        j += 1
                    i = j - 1  # nhảy bước

                # ------------------ Upload file ------------------
                elif step.startswith("upload file"):
                    parts = step.replace("upload file", "").split("vào ô")
                    file_path2 = parts[0].strip()
                    selector = parts[1].strip()
                    elem = driver.find_element(By.CSS_SELECTOR, selector)
                    elem.send_keys(file_path2)

                # ------------------ Click ------------------
                elif step.startswith("click nút"):
                    target = step.replace("click nút", "").strip()
                    try:
                        if target.startswith(("button", "input", ".", "#", "[")):
                            elem = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, target))
                            )
                        else:
                            xpath = f"//button[normalize-space()='{target}']"
                            elem = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, xpath))
                            )
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                        time.sleep(0.3)
                        try:
                            elem.click()
                        except:
                            driver.execute_script("arguments[0].click();", elem)
                    except Exception as e:
                        raise Exception(f"Không click được nút: {target} ({e})")

                # ------------------ Chọn option ------------------
                elif step.startswith("chọn option"):
                    parts = step.replace("chọn option", "").split("trong ô")
                    option_text = parts[0].strip()
                    selector = parts[1].strip()
                    select_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    Select(select_elem).select_by_visible_text(option_text)

                # ------------------ Kiểm tra chứa text ------------------
                elif step.startswith("kiểm tra chứa text"):
                    expected = step.replace("kiểm tra chứa text", "").strip()
                    body = driver.find_element(By.TAG_NAME, "body").text
                    if expected in body:
                        log(f"✅ PASS: tìm thấy '{expected}'")
                    else:
                        raise AssertionError(f"Không tìm thấy '{expected}' trong trang")

                # ------------------ Kiểm tra URL ------------------
                elif step.startswith("kiểm tra url chứa"):
                    expected = step.replace("kiểm tra url chứa", "").strip()
                    if expected in driver.current_url:
                        log(f"✅ PASS: URL chứa '{expected}'")
                    else:
                        raise AssertionError(f"URL '{driver.current_url}' không chứa '{expected}'")

                # ------------------ Kiểm tra Title ------------------
                elif step.startswith("kiểm tra title chứa"):
                    expected = step.replace("kiểm tra title chứa", "").strip()
                    if expected in driver.title:
                        log(f"✅ PASS: Title chứa '{expected}'")
                    else:
                        raise AssertionError(f"Title '{driver.title}' không chứa '{expected}'")

                else:
                    log(f"⚠️ Không hiểu bước: {step}")

                passed += 1

            except Exception as e:
                failed += 1
                ts = int(time.time())
                screenshot = f"screenshots/fail_{ts}.png"
                capture_with_error(driver, screenshot, str(e))
                log(f"❌ FAIL: {step} -> {e} (ảnh lưu tại {screenshot})")

                # 👉 Tạo GitHub Issue
                issue_title = f"[Test Fail] {os.path.basename(file_path)} - Step lỗi"
                issue_body = f"❌ Testcase: `{file_path}`\n\nStep: `{step}`\n\nError: {e}"
                create_github_issue(issue_title, issue_body, screenshot)

            time.sleep(1)
            i += 1

        log(f"\n📊 Kết quả: {passed}/{total} bước PASS, {failed} FAIL\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    for file in os.listdir("tests"):
        if file.endswith(".txt"):
            log(f"\n🚀 Chạy testcase: {file}")
            run_testcase(os.path.join("tests", file))
