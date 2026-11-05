import glob
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import markdown

# ==================== 基础配置 ====================
MAIL_HOST = "smtp.qq.com"
MAIL_PORT = 465  # QQ邮箱 SSL 端口

SENDER_EMAIL = "ttflyy@vip.qq.com"
RECEIVER_EMAIL = "ttflyy@vip.qq.com"

MAIL_PASS = os.environ.get("MAIL_PASS")
# ==================================================

if not MAIL_PASS:
  print("错误: 未检测到 MAIL_PASS 环境变量！")
  exit(1)

# 同时在根目录的 _posts 和 docs/_posts 下寻找 md 文件
list_of_files = glob.glob("_posts/*.md") + glob.glob("docs/_posts/*.md")
if not list_of_files:
  print("错误: 没有找到任何日报文件！")
  exit(1)

latest_file = max(list_of_files, key=os.path.getctime)
print(f"正在发送的日报文件是: {latest_file}")

# 读取 Markdown 文件内容
with open(latest_file, "r", encoding="utf-8") as f:
  md_content = f.read()

# 将 Markdown 转换为 HTML
html_body = markdown.markdown(md_content, extensions=["extra", "codehilite"])

# 针对 QQ 邮箱不友好的 class 过滤机制，改用全局标签样式（Tag Selectors）
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  /* 邮件整体背景 */
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #2d3748;
    background-color: #f7fafc;
    margin: 0;
    padding: 20px;
  }}
  /* 邮件核心内容卡片，直接通过 div 标签和样式控制 */
  div {{
    max-width: 750px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
  }}
  h1, h2, h3 {{
    color: #1a202c;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 24px;
  }}
  p {{
    margin: 12px 0;
    color: #2d3748;
  }}
  a {{
    color: #3182ce;
    text-decoration: none;
  }}
  a:hover {{
    text-decoration: underline;
  }}
  blockquote {{
    border-left: 4px solid #3182ce;
    margin: 12px 0;
    padding: 8px 15px;
    color: #4a5568;
    background: #ebf8ff;
  }}
  code {{
    background: #edf2f7;
    color: #c53030;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 90%;
  }}
  hr {{
    border: none;
    border-top: 1px dashed #e2e8f0;
    margin: 25px 0;
  }}
  ul, ol {{
    padding-left: 20px;
  }}
</style>
</head>
<body>
  <div>
    {html_body}
  </div>
</body>
</html>
"""

# 组装 HTML 格式邮件
message = MIMEText(styled_html, "html", "utf-8")
message["From"] = f"Horizon Digest <{SENDER_EMAIL}>"
message["To"] = RECEIVER_EMAIL
message["Subject"] = f"Horizon Daily AI Digest - {os.path.basename(latest_file)}"

# 连接服务器并发送
try:
  smtp_obj = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
  smtp_obj.login(SENDER_EMAIL, MAIL_PASS)
  smtp_obj.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], message.as_string())
  smtp_obj.quit()
  print("邮件发送成功！")
except Exception as e:
  print(f"邮件发送失败: {e}")
