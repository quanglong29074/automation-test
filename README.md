# Automation Test Project

This project is an automation testing framework using Selenium and browser automation tools to execute test cases defined in text files.

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Git (to clone the repository if needed)

### 2. Clone the Repository (if not already done)
```bash
git clone git@github.com:quanglong29074/automation-test.git
cd automation-test
```

### 3. Create and Activate Virtual Environment
Create a virtual environment to manage dependencies:
```bash
python -m venv venv
```

Activate the virtual environment:
- On Linux/macOS:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\\Scripts\\activate
  ```

### 4. Install Dependencies
Install the required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

The dependencies include:
- `selenium`: For web browser automation
- `webdriver-manager`: For managing browser drivers
- `python-dotenv`: For loading environment variables
- `requests`: For HTTP requests
- `pygithub`: For GitHub API interactions
- `opencv-python`: For computer vision tasks
- `ffmpeg-python`: For video processing
- `mss`: For screenshots
- `browser-use`: Custom browser automation library

### 5. Configure Environment Variables
Copy the `.env` file and fill in any required variables (e.g., API keys, credentials). The file should be in the root directory.

## Running Tests

### Execute a Test Case
The project uses `runner.py` to run test cases asynchronously.

To run the sample test case:
```bash
python runner.py
```

This will execute `tests/testcase1.txt` using the browser automation agent.

### Run a Custom Test Case
Modify `runner.py` to point to a different file, or update the `run_testcase_from_file` call:
```python
asyncio.run(run_testcase_from_file("tests/your_testcase.txt"))
```

Ensure the test case file follows the standard format described below.

### Browser Configuration
- The browser runs in non-headless mode (visible window) by default.
- Set `headless=True` in `BrowserProfile` for headless execution.

## Writing Test Cases

Test cases are written in plain text files (e.g., `.txt`) following a structured format. Refer to `tests/testcase1.txt` for the sample.

### Standard Format

```
[TestCase]
Name: [Short descriptive name]
Objective: [Brief description of what the test verifies]

[Tasks]

Task 1: [Task name]
Steps:
1. [Step 1 description]
2. [Step 2 description]
...
ExpectedResult: [What should happen if successful]
Dependency: [Previous task number or "None"]

Task 2: [Task name]
Steps:
1. [Step 1 description]
...
ExpectedResult: [Expected outcome]
Dependency: [Task 1 (or relevant dependency)]
...
```

### Guidelines
- **Name**: Keep it concise and descriptive (e.g., "Đăng nhập và tạo sản phẩm mới").
- **Objective**: Explain the high-level goal (e.g., "Xác minh rằng người dùng có thể đăng nhập thành công và sau đó tạo được sản phẩm mới").
- **[Tasks]**: Break down into sequential tasks. Each task builds on previous ones.
  - **Steps**: Numbered list of actions (e.g., "Mở trang https://ct360.io/Members/Sign-in", "Nhập username 'validUser'").
    - Use specific details like URLs, input values, button names.
    - For interactions: Specify clicks, inputs, uploads (e.g., "Upload ảnh sản phẩm 'shirt.jpg'").
  - **ExpectedResult**: Clear success criteria (e.g., "Hệ thống điều hướng đến trang https://ct360.io/ và hiển thị Dashboard.", "Thông báo 'Tạo sản phẩm thành công' hiển thị").
  - **Dependency**: Reference prior tasks (e.g., "Task 1 (phải login thành công)") or "None" for the first task.
- Use Vietnamese for consistency with the sample, unless specified otherwise.
- Save files in the `tests/` directory.
- Ensure steps are executable by the automation agent (e.g., browser navigation, form filling).

### Example from testcase1.txt
```
[TestCase]
Name: Đăng nhập và tạo sản phẩm mới
Objective: Xác minh rằng người dùng có thể đăng nhập thành công và sau đó tạo được sản phẩm mới.

[Tasks]

Task 1: Đăng nhập hệ thống
Steps:
1. Mở trang https://ct360.io/Members/Sign-in
2. Nhập username "validUser"
3. Nhập password "validPass123"
4. Click nút Log in
ExpectedResult: Hệ thống điều hướng đến trang https://ct360.io/ và hiển thị Dashboard.
Dependency: None

Task 2: Mở form tạo sản phẩm
Steps:
1. Truy cập menu "Sản phẩm"
2. Click nút "Tạo sản phẩm"
ExpectedResult: Hiển thị form tạo sản phẩm.
Dependency: Task 1 (phải login thành công)

Task 3: Nhập thông tin và lưu sản phẩm
Steps:
1. Nhập tên sản phẩm "Áo Thun Test"
2. Nhập giá "199000"
3. Upload ảnh sản phẩm "shirt.jpg"
4. Click nút "Lưu"
ExpectedResult: Thông báo "Tạo sản phẩm thành công" hiển thị và sản phẩm xuất hiện trong danh sách.
Dependency: Task 2 (form tạo sản phẩm đã hiển thị)
```

## Troubleshooting
- Ensure the browser (e.g., Chrome) is installed and compatible.
- Check `.env` for any required credentials.
- If the agent fails, review console output for errors.

## Project Structure
- `requirements.txt`: Dependencies
- `runner.py`: Main runner script
- `.env`: Environment variables
- `tests/`: Test case files (e.g., `testcase1.txt`)

For contributions, follow the test case format and update this README as needed.
