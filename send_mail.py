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

# 腾讯/主流大厂视觉设计语言 (大厂级 CSS 样式)
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  /* 全局背景：采用科技感极浅灰 */
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.65;
    color: #374151;
    background-color: #f3f4f6;
    margin: 0;
    padding: 24px 12px;
    -webkit-font-smoothing: antialiased;
  }}
  
  /* 主容器卡片化设计 */
  div {{
    max-width: 680px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 36px 32px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid #e5e7eb;
  }}

  /* 主标题 (H1, H2) */
  h1, h2 {{
    color: #111827;
    font-weight: 700;
    letter-spacing: -0.025em;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 10px;
    margin-top: 10px;
    margin-bottom: 24px;
  }}

  /* 文章小标题 (H3)：突出显示 + 优雅的高亮蓝 */
  h3 {{
    color: #1e293b;
    font-size: 18px;
    font-weight: 600;
    margin-top: 32px;
    margin-bottom: 12px;
    line-height: 1.4;
  }}

  /* 文章超链接 */
  h3 a, a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
  }}
  a:hover {{
    text-decoration: underline;
    color: #1d4ed8;
  }}

  /* 段落文本：优化间距与字号 */
  p {{
    margin: 10px 0;
    font-size: 15px;
    color: #4b5563;
  }}

  /* 加粗文本：提升视觉对比度 */
  strong {{
    color: #111827;
    font-weight: 600;
  }}

  /* 引用块/背景方案块：现代化左边框卡片 */
  blockquote {{
    border-left: 4px solid #3b82f6;
    margin: 16px 0;
    padding: 12px 18px;
    color: #1f2937;
    background-color: #eff6ff;
    border-radius: 0 8px 8px 0;
    font-size: 14.5px;
  }}

  /* 标签与评分代码块高亮 */
  code {{
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 3px 8px;
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 13px;
    border: 1px solid #e2e8f0;
  }}

  /* 分割线 */
  hr {{
    border: none;
    border-top: 1px solid #f3f4f6;
    margin: 36px 0;
  }}

  /* 列表项优化 */
  ul, ol {{
    padding-left: 20px;
    margin: 12px 0;
    color: #4b5563;
  }}
  li {{
    margin-bottom: 6px;
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
