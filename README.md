# 🤖 Hisse Senedi Alım-Satım Botu

Bu proje, Python kullanarak basit bir hisse senedi alım-satım botu oluşturur. 5-günlük hareketli ortalama stratejisi ile backtesting yapar ve sonuçları görselleştirir.

## ✨ Özellikler

- 📊 **5-günlük hareketli ortalama stratejisi**
- 🔄 **Otomatik backtesting**
- 📈 **Görselleştirme ile sonuç analizi**
- 💰 **Portföy değeri takibi**
- 🎯 **Al/sat sinyalleri**
- 📋 **Detaylı işlem raporu**

## 🚀 Hızlı Başlangıç

### Gereksinimler
```bash
pip install pandas numpy matplotlib
```

### Kurulum
1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/trading_bot.git
cd trading_bot
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Programı çalıştırın:
```bash
python main.py
```

## 📊 Nasıl Çalışır

### Strateji
- **Al Sinyali**: Hisse fiyatı > 5-günlük hareketli ortalama
- **Sat Sinyali**: Hisse fiyatı < 5-günlük hareketli ortalama

### Backtesting
- Başlangıç sermayesi: 10,000 TL
- Otomatik al/sat işlemleri
- Portföy değeri takibi
- Performans analizi

## 📈 Sonuçlar

Program şu bilgileri sağlar:
- 💰 Final sermaye
- 📈 Toplam getiri yüzdesi
- 🔄 Toplam işlem sayısı
- 📅 İşlem tarihleri
- 📊 Görsel grafikler

## 🛠️ Teknolojiler

- **Python 3.8+**
- **pandas** - Veri işleme
- **numpy** - Matematiksel hesaplamalar
- **matplotlib** - Görselleştirme

## 📁 Proje Yapısı
