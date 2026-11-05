import os
import smtplib
import glob
from email.header import Header
from email.mime.text import MIMEText

# ==================== 基础配置 ====================
MAIL_HOST = "smtp.qq.com"
MAIL_PORT = 465  # QQ邮箱 SSL 端口

# 【新手直接在这里填你的邮箱】
SENDER_EMAIL = "ttflyy@vip.qq.com"   # 例如：12345678@qq.com
RECEIVER_EMAIL = "ttflyy@vip.qq.com" # 收件人通常也是你自己

# 授权码依然从 GitHub 安全密钥中读取，不在代码里明文暴露
MAIL_PASS = os.environ.get("MAIL_PASS") 
# ==================================================

if not MAIL_PASS:
    print("错误: 未检测到 MAIL_PASS 环境变量！")
    exit(1)

# 自动查找 docs/_posts/ 目录下最新的一篇日报文件
# 同时在根目录的 _posts 和 docs/_posts 下寻找 md 文件
list_of_files = glob.glob("_posts/*.md") + glob.glob("docs/_posts/*.md")
if not list_of_files:
    print("错误: 没有找到任何日报文件！")
    exit(1)

latest_file = max(list_of_files, key=os.path.getctime)
print(f"正在发送的日报文件是: {latest_file}")

# 读取文件内容
with open(latest_file, "r", encoding="utf-8") as f:
    content = f.read()

# 组装邮件
message = MIMEText(content, "plain", "utf-8")
# 使用纯英文昵称加邮箱，绝对不会触发 ASCII 编码错误
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
