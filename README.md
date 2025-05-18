# ⚓ İki Oyunculu UDP Battleship Oyunu

Bu proje, Python ve UDP soket programlama kullanılarak geliştirilmiş iki oyunculu klasik **Battleship (Savaş Gemisi)** oyunudur. Her oyuncu kendi tahtasına gemilerini yerleştirir ve rakibinin gemilerini vurmaya çalışır.

## 🎮 Oyun Özellikleri

- 🔁 Gerçek zamanlı, çift yönlü haberleşme (UDP üzerinden)
- 🎯 Hit (isabet) ve Miss (ıskalama) hesaplama
- 📡 Sunucu ve istemci ayrımı
- 🧠 Rastgele gemi yerleşimi
- 🗺️ ASCII tabanlı 10x10 oyun tahtası

## 🗂️ Dosya Yapısı

| Dosya | Açıklama |
|-------|----------|
| `server.py` | Oyun sunucusu, tüm haberleşmeyi yönetir |
| `client.py` | Oyuncunun oyun arayüzü, giriş/çıkış ve hamleleri içerir |

## 🚀 Kurulum ve Çalıştırma

### 1️⃣ Sunucu (Server)

1. `server.py` dosyasını aç.
2. IP adresini belirt:
   ```python
   HOST = '192.168.X.X'  # Sunucu bilgisayarının yerel IP'si
