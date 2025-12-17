📧 My Mails – Gmail Desktop Client

My Mails is a simple desktop Gmail client built with Python, Tkinter, and the Gmail API.
It allows you to send emails and view your inbox in a clean, card-based interface.

🚀 Features

✉️ Send email via Gmail

📬 View inbox messages (card UI)

🔄 Refresh inbox without freezing the UI (threading)

⏱️ Live clock on the home screen

🎨 Modern navy themed interface

🧭 Page-based navigation (Home / Compose / Inbox)

📌 Prerequisites

This project uses the Gmail API, which requires Google Cloud OAuth setup.
Before running this app, you must follow the official Gmail API setup guide:

Bu çok iyi bir nokta yakalaman 👍
Evet, projeyi ilk kez açan herkes bu hatayı alacak ve bu beklenen / normal bir durum. Bunu hem README’de açıklamamız hem de istersek kodda daha anlaşılır hale getirmemiz gerekir.

Aşağıda 3 parçalı net çözüm veriyorum:

1️⃣ Bu hata NEDEN oluyor? (kısa ve net açıklama)

Hata:

FileNotFoundError: No such file or directory: 'credentials.json'


Sebep:

Gmail API OAuth gerektirir

credentials.json dosyası Google Cloud Console tarafından üretilir

Bu dosya bilerek GitHub’a konmaz

İlk kez açan kullanıcıda doğal olarak yoktur

📌 Yani bu bir bug değil, kurulum adımı eksik.

2️⃣ README’ye EKLENMESİ GEREKEN bölüm (çok önemli)

README’ye aşağıdaki bölümü aynen eklemeni öneriyorum:

⚠️ First Run – Common Error (credentials.json)

If you run the project for the first time and see this error:

FileNotFoundError: No such file or directory: 'credentials.json'


This is expected behavior.

This project uses the Gmail API, which requires OAuth credentials provided by Google.
The file credentials.json is not included in the repository for security reasons.

✅ How to fix

Read and follow the official Gmail API Quickstart:
https://developers.google.com/workspace/gmail/api/quickstart/python

Create a Google Cloud project and enable Gmail API

Create an OAuth 2.0 Client ID

Download the generated credentials.json

Place credentials.json in the project root directory


👉 Google Official Quickstart (Python)
https://developers.google.com/workspace/gmail/api/quickstart/python?hl=tr

✔️ This quickstart shows how to:

Enable the Gmail API

Configure OAuth credentials

Create credentials.json

Generate the first token.json

💡 You MUST complete that first.
If credentials.json is missing or invalid, the app won’t authenticate.

🧠 Tech Stack

Python 3

Tkinter (GUI)

Google Gmail API

OAuth 2.0

Threading (for responsive inbox loads)

📂 Project Structure
my-mails/
│
├─ app.py                # Tkinter desktop application
├─ quickstart.py         # Gmail API logic
├─ credentials.json      # Google OAuth credentials (NOT committed)
├─ Tokens/
│   └─ token.json        # OAuth token (NOT committed)
├─ README.md
├─ .gitignore

▶️ How to Run

Follow the Gmail API Quickstart (link above)

Place credentials.json in the project root

Run:

python app.py


On first run, your browser will open for Google login and OAuth consent.
After success, Tokens/token.json will be created automatically.

⚠️ SECURITY & GIT IGNORE

These files must NOT be committed:

credentials.json
Tokens/


Add this to .gitignore:

# OAuth
credentials.json
Tokens/
token.json

# Python
__pycache__/
*.pyc
*.pyo
.venv/

🛠️ Future Improvements

📩 Email detail view

⭐ Star / delete messages

🔔 New mail notifications

📄 Pagination (Load more)

📎 Attachment support