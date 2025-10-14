# Hisse Senedi Alım-Satım Botu

Bu proje, Python kullanarak basit bir hisse senedi alım-satım botu oluşturur.

## Özellikler

- 5-günlük hareketli ortalama stratejisi
- Backtesting ile performans analizi
- Görselleştirme ile sonuç analizi
- Temiz ve anlaşılır kod yapısı

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Programı çalıştırın:
```bash
python main.py
```

## Nasıl Çalışır

1. Örnek hisse senedi verisi oluşturur
2. 5-günlük hareketli ortalamayı hesaplar
3. Al/sat sinyalleri üretir
4. Backtesting yapar
5. Sonuçları grafikle gösterir

## Strateji

- **Al Sinyali**: Hisse fiyatı > 5-günlük MA
- **Sat Sinyali**: Hisse fiyatı < 5-günlük MA