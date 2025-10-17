# 🎵 YT-MP3 Downloader (Terminal Tool)

Một công cụ nhỏ gọn, chạy bằng **Python**, giúp bạn **tải nhạc từ YouTube thành file MP3** chất lượng cao (320kbps) chỉ với **một dòng link**.

Giao diện được thiết kế tối giản, dễ nhìn, thân thiện trên terminal.

---

## 📸 Screenshot
![Screenshot](https://i.postimg.cc/cC5WJxW8/Screenshot-2025-10-17-153823.png)

## 🚀 Tính năng

- 🎧 Tải **YouTube → MP3** với chất lượng tốt nhất tự động.
- 💾 Lưu file vào thư mục **Downloads** mặc định của Windows.
- 📊 Hiển thị **thanh tiến trình tải** gọn, rõ ràng.
- 🧠 Không cần cài đặt phức tạp hoặc chọn tùy chọn thủ công.
- 🖤 Giao diện sạch, đẹp, thân thiện terminal (dùng thư viện `rich`).

---

## 🧩 Yêu cầu

- Python **3.10** hoặc mới hơn
- Thư viện:
  ```bash
  pip install yt-dlp rich requests
  ```
- FFmpeg (dùng để chuyển định dạng sang MP3)
  ```bash
  winget install ffmpeg
  ```
  hoặc tải thủ công tại: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

---

## 💻 Cách cài đặt

1. Tải file `app.py` về máy.
2. Mở **Command Prompt** hoặc **PowerShell**.
3. Di chuyển đến thư mục chứa file:
   ```bash
   cd C:\duong_dan_toi_file\
   ```
4. Chạy tool:
   ```bash
   python app.py
   ```

---

## 🧠 Cách sử dụng

1. Chạy chương trình.
2. Khi được hỏi, **dán link YouTube** bạn muốn tải.
3. Tool sẽ:
   - Tự động chọn chất lượng âm thanh tốt nhất.
   - Tải file MP3.
   - Hiển thị thanh tiến trình tải.
4. Khi hoàn tất, terminal sẽ hiển thị:
   - ✅ Tên file MP3
   - 💾 Dung lượng
   - 📁 Vị trí lưu (thư mục `Downloads`)

---

## 📂 Ví dụ sử dụng

```bash
> python app.py

🎵 YT-MP3 Downloader

Nhập link YouTube: https://www.youtube.com/watch?v=dQw4w9WgXcQ
📁 File sẽ được lưu tại: C:\Users\<tên_user>\Downloads

Đang tải... ██████████████████████ 100%

✅ Tải thành công!

Tên file: Rick Astley - Never Gonna Give You Up.mp3
Kích thước: 5.23 MB
Vị trí: C:\Users\<tên_user>\Downloads
```

---

## ⚠️ Lưu ý pháp lý

> Công cụ này chỉ nên được dùng để tải nội dung mà **bạn có quyền tải xuống**, chẳng hạn:
>
> - Nhạc / video bạn sở hữu hoặc có bản quyền cho phép.
> - Nội dung thuộc **public domain**.
> - Video có **Creative Commons License**.

Việc tải nội dung vi phạm bản quyền có thể vi phạm luật tại quốc gia của bạn.  
Người tạo tool không chịu trách nhiệm cho việc sử dụng sai mục đích.

---

## 🧱 Tùy chọn nâng cao (nếu muốn)

- Đóng gói thành file `.exe` chạy được trên Windows (không cần Python):
  ```bash
  pip install pyinstaller
  pyinstaller --onefile ytmp3_simple.py
  ```
  Sau khi chạy, bạn sẽ có file `dist/ytmp3_simple.exe`.

---

## 🧑‍💻 Tác giả

**YT-MP3 Downloader** — vibe-coding bằng Python bởi _Sigma Sybau Pro Vip 68_  
💬 Liên hệ / góp ý: [GitHub Issues](https://github.com/)

---

⭐ _Nếu bạn thấy tool hữu ích, đừng quên tặng một star cho repo nhé!_
