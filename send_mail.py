import glob
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import markdown

# ==================== 基础配置 ====================
MAIL_HOST = "smtp.qq.com"
MAIL_PORT = 465

SENDER_EMAIL = "ttflyy@vip.qq.com"
RECEIVER_EMAIL = "ttflyy@vip.qq.com"
MAIL_PASS = os.environ.get("MAIL_PASS")

if not MAIL_PASS:
  print("错误: 未检测到 MAIL_PASS 环境变量！")
  exit(1)

list_of_files = glob.glob("_posts/*.md") + glob.glob("docs/_posts/*.md")
if not list_of_files:
  print("错误: 没有找到任何日报文件！")
  exit(1)

latest_file = max(list_of_files, key=os.path.getctime)
print(f"正在发送的日报文件是: {latest_file}")

with open(latest_file, "r", encoding="utf-8") as f:
  md_content = f.read()

html_body = markdown.markdown(md_content, extensions=["extra", "codehilite"])

# 极致护眼、大留白、高条理的现代化邮件模板
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  /* 整体背景：采用极为温和、不刺眼的护眼米色羊皮纸底色 */
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.85;
    color: #2d3748;
    background-color: #f6f4ee;
    margin: 0;
    padding: 30px 15px;
    -webkit-font-smoothing: antialiased;
  }}
  
  /* 核心内容区：卡片式悬浮设计，留白充足，告别拥挤 */
  div.email-container {{
    max-width: 720px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 45px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid #e8e4dc;
  }}

  /* 顶部目录与标题区整理 */
  h1, h2 {{
    color: #1a202c;
    font-weight: 700;
    font-size: 22px;
    letter-spacing: -0.02em;
    border-bottom: 2px solid #3182ce;
    padding-bottom: 12px;
    margin-top: 15px;
    margin-bottom: 28px;
  }}

  /* 文章小标题：清晰的层级与舒适的间距 */
  h3 {{
    color: #2b6cb0;
    font-size: 17px;
    font-weight: 600;
    margin-top: 38px;
    margin-bottom: 14px;
    line-height: 1.5;
  }}

  h3 a {{
    color: #2b6cb0;
    text-decoration: none;
  }}
  h3 a:hover {{
    text-decoration: underline;
  }}

  /* 正文段落：行高拉开，彻底解决行间距太近的问题 */
  p {{
    margin: 14px 0;
    font-size: 15px;
    color: #4a5568;
    line-height: 1.85;
  }}

  strong {{
    color: #1a202c;
    font-weight: 600;
  }}

  /* 重点摘要/背景方案：护眼浅蓝灰色引用块 */
  blockquote {{
    border-left: 4px solid #3182ce;
    margin: 18px 0;
    padding: 14px 20px;
    color: #2d3748;
    background-color: #f0f4f8;
    border-radius: 0 6px 6px 0;
    font-size: 14.5px;
  }}

  /* 标签样式 */
  code {{
    background-color: #edf2f7;
    color: #c53030;
    padding: 3px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 12.5px;
    border: 1px solid #e2e8f0;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 40px 0;
  }}

  ul, ol {{
    padding-left: 22px;
    margin: 14px 0;
    color: #4a5568;
  }}
  li {{
    margin-bottom: 8px;
    line-height: 1.7;
  }}
</style>
</head>
<body>
  <div class="email-container">
    {html_body}
  </div>
</body>
</html>
"""

message = MIMEText(styled_html, "html", "utf-8")
message["From"] = f"Horizon Digest <{SENDER_EMAIL}>"
message["To"] = RECEIVER_EMAIL
message["Subject"] = f"Horizon Daily AI Digest - {os.path.basename(latest_file)}"

try:
  smtp_obj = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
  smtp_obj.login(SENDER_EMAIL, MAIL_PASS)
  smtp_obj.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], message.as_string())
  smtp_obj.quit()
  print("邮件发送成功！")
except Exception as e:
  print(f"邮件发送失败: {e}")
