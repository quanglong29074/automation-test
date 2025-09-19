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

This will execute `tests/testcase1.yaml` using the browser automation agent.

### Run a Custom Test Case
Modify `runner.py` to point to a different file, or update the `run_testcase_from_file` call:
```python
asyncio.run(run_testcase_from_file("tests/your_testcase.yaml"))
```

Ensure the test case file follows the standard format described below.

### Browser Configuration
- The browser runs in non-headless mode (visible window) by default.
- Set `headless=True` in `BrowserProfile` for headless execution.

## Writing Test Cases

Test cases are written in YAML files (`.yaml`) following a structured format. Refer to `tests/testcase1.yaml` for the sample. Each file contains a list of individual test cases.

### Standard Format

A YAML file is a list of test case objects. Each test case has the following keys:

- `id`: Unique identifier (e.g., "TC_LOGIN_001")
- `title`: Descriptive name of the test case
- `precondition`: Conditions that must be met before running the test (e.g., "Trang login đã mở")
- `steps`: List of action steps as strings (e.g., "- mở trang 'https://example.com'")
- `expected`: Expected outcome if the test passes
- `priority`: Priority level (e.g., "high", "medium", "low")

### Guidelines
- **id**: Use a unique, descriptive ID following a naming convention (e.g., TC_[MODULE]_[NUMBER]).
- **title**: Concise description in Vietnamese (e.g., "Đăng nhập thành công").
- **precondition**: Specify setup requirements or dependencies (e.g., "Người dùng đã đăng nhập thành công").
- **steps**: Bullet list of actions starting with verbs like "mở", "nhập", "click". Include specific details:
  - URLs for navigation.
  - Values for inputs (e.g., usernames, passwords).
  - Element identifiers for interactions (e.g., button names, fields).
- **expected**: Clear, verifiable success criteria (e.g., URL changes, UI elements displayed, messages shown).
- **priority**: Classify as "high", "medium", or "low" based on importance.
- Use Vietnamese for consistency with the sample.
- Save files in the `tests/` directory with `.yaml` extension.
- Ensure steps are executable by the automation agent (e.g., browser actions, form interactions).
- Multiple test cases can be defined in one YAML file as a list.

### Example from testcase1.yaml
```yaml
- id: TC_LOGIN_001
  title: Đăng nhập thành công
  precondition: Trang login đã mở
  steps:
    - mở trang "https://staging.trung-rong.pages.dev/login"
    - nhập username "jehatik"
    - nhập password "123456"
    - click nút "Log in"
  expected: Hệ thống điều hướng đến "https://staging.trung-rong.pages.dev/" và hiển thị Dashboard
  priority: high

- id: TC_PROFILE_001
  title: Truy cập trang Profile
  precondition: Người dùng đã đăng nhập thành công
  steps:
    - mở trang "https://staging.trung-rong.pages.dev/profile"
  expected: Trang Profile hiển thị với form chỉnh sửa thông tin cá nhân
  priority: medium

- id: TC_PROFILE_002
  title: Cập nhật thông tin Discord
  precondition: Trang Profile đã hiển thị
  steps:
    - trong mục "Social Media", nhập vào trường Discord giá trị "https://discord.gg/discord"
    - click nút "Save"
  expected: Hiển thị thông báo "Lưu thành công" và trường Discord hiển thị giá trị vừa nhập
  priority: high
```

## Troubleshooting
- Ensure the browser (e.g., Chrome) is installed and compatible.
- Check `.env` for any required credentials.
- If the agent fails, review console output for errors.

## Project Structure
- `requirements.txt`: Dependencies
- `runner.py`: Main runner script
- `.env`: Environment variables
- `tests/`: Test case files (e.g., `testcase1.yaml`)

For contributions, follow the test case format and update this README as needed.
