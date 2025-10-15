# 🤖 Hisse Senedi Alım-Satım Botu (2025 Güncel)

Python ile geliştirilen, 2025’in başından bugüne veri çekebilen, strateji, risk yönetimi, optimizasyon ve web arayüzü sunan gelişmiş alım-satım botu.

- 👤 Geliştirici: Güler Göçmen
- 🖥️ Ortam: Windows 10 (Python 3.10), VS Code
- 📅 Veri Aralığı (varsayılan): 2025-01-01 → Bugün
- 💰 Varsayılan Sermaye: 10.000 TL

---

## ✨ Özellikler
- 🔌 Gerçek veri (Yahoo Finance, `yfinance`)
- 🧠 Strateji: SMA(5/10/20), RSI, MACD, Bollinger, Stochastic
- 🛡️ Risk: Stop-Loss ve Take-Profit
- 🔍 Optimizasyon: SMA periyodu taraması
- 📈 Görseller: Matplotlib (CLI) + Plotly (Streamlit)
- 🌐 Web Arayüzü: Streamlit (parametrelerle oynayabilme)

---

## 📁 Proje Yapısı 

SMA5_BACKTEST_PROJECT/
│
├── main2.py              # Gelişmiş al-sat botu (CLI)
├── app2.py               # Streamlit web arayüzü
├── requirements2.txt     # Gerekli kütüphaneler
├── README.md             # Proje açıklaması
├── .gitignore
└── .venv/                # Sanal ortam (GitHub’a dahil edilmez)


---

## ⚙️ Kurulum
1) Projeyi klasöre ekleyin (VS Code > Open Folder ile açın).
2) Gerekli paketler:
```bash
pip install -r requirements.txt
# veya
pip install pandas numpy matplotlib yfinance ta plotly streamlit scikit-learn requests
```

---

## 🚀 Çalıştırma

### A) Komut Satırı (main.py)
```bash
cd "C:\Users\Güler Göçmen\trading_bot"
python main.py
```
- Sembol seçimi sorar (AAPL/GOOGL/MSFT/TSLA veya özel sembol).
- 2025-01-01’den bugüne veri çeker → indikatörleri hesaplar → sinyal üretir → backtest yapar → grafik gösterir.

### B) Web Arayüzü (app.py)
```bash
cd "C:\Users\Güler Göçmen\trading_bot"
streamlit run app.py
```
- Tarayıcı: http://localhost:8501
- Sidebar’dan sembol, periyot (1y/6mo/3mo/1mo), SMA/RSI, Stop-Loss/Take-Profit, sermaye ayarlanır.
- İnteraktif fiyat, sinyal, RSI, portföy grafikleri ve işlem tablosu.

---

## 🧠 Strateji Özeti
- Basit kural: Close > SMA → Al, Close < SMA → Sat
- Kombine sinyal (ağırlıklar): SMA 0.5, RSI 0.3, MACD 0.2
- Risk yönetimi: Stop-Loss varsayılan %5, Take-Profit varsayılan %10
- Optimizasyon: SMA aralığı (örn. 3–20) taranır, en iyi getiri seçilir

---

## 🔧 Hızlı Parametreler
- CLI: `main.py` içinde
  - `initial_capital=10000`
  - `stop_loss=0.05`, `take_profit=0.10`
  - Veri başlangıcı: `"2025-01-01"`
- Web: `app.py` içindeki Streamlit Sidebar’dan değiştirilebilir.

---

## 📊 Çıktılar
- Terminal özeti:
  - Başlangıç/Final sermaye, toplam getiri (%), işlem sayısı, işlem nedenleri (Signal/Stop-Loss/Take-Profit)
- Grafikler:
  - Fiyat + SMA + Bollinger + Al/Sat işaretleri
  - RSI + MACD
  - Portföy değeri (başlangıç çizgisi ile)

---

## 🩺 Sorun Giderme (Windows)
- “dosya bulunamadı”:
  ```bash
  cd "C:\Users\Güler Göçmen\trading_bot"
  python main.py
  ```
- Türkçe karakter/boşluk yolu:
  - Komutlarda yolu tırnak içine alın (yukarıdaki gibi).
- Yahoo Finance veri boş:
  - Sembol doğru mu? Bölge son ekleri (örn. BIST için `TUPRS.IS`) gerekebilir.
- Grafik açılmıyorsa:
  - `pip install matplotlib`
- Streamlit açılmıyorsa:
  - `streamlit run app.py` sonrası tarayıcıyı kontrol edin (http://localhost:8501).

---

## 🗺️ Yol Haritası
- [ ] Ek metrikler (Sharpe, Max Drawdown)
- [ ] Çoklu sembol portföy backtest
- [ ] İşlem maliyeti ve slippage simülasyonu
- [ ] Basit ML tabanlı stratejiler (sklearn)
- [ ] PDF/HTML raporlama

---

## 🛡️ Uyarı
Bu proje eğitim amaçlıdır, finansal tavsiye değildir. Gerçek yatırım kararları için profesyonel danışmanlık alınız.

---

## 👤 İletişim
- GitHub: (https://github.com/glr35)
- Issues: Hata/öneri için repo “Issues” sekmesini kullanın



| Özellik | Açıklama |
|----------|----------|
| 📊 Strateji | SMA, RSI, MACD, Bollinger, Stochastic |
| 🧮 Optimizasyon | SMA aralığı, en iyi parametre seçimi |
| 💻 Web Arayüzü | Streamlit + Plotly |
| 🔢 Kütüphaneler | pandas, numpy, matplotlib, scikit-learn, ta |
