"""
Hisse Senedi Alım-Satım Botu
Basit 5-günlük hareketli ortalama stratejisi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class TradingBot:
    def __init__(self, initial_capital=10000):
        """Trading Bot sınıfını başlatır"""
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.portfolio_values = []
        self.trades = []
        
    def create_sample_data(self):
        """Örnek hisse senedi verisi oluşturur"""
        print("📊 Örnek veri oluşturuluyor...")
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)
        
        data = pd.DataFrame({
            'Date': dates,
            'Close': prices
        })
        print(f"✅ {len(data)} günlük veri oluşturuldu")
        return data
    
    def calculate_sma(self, data, window=5):
        """5-günlük hareketli ortalama hesaplar"""
        data['SMA_5'] = data['Close'].rolling(window=window).mean()
        return data
    
    def generate_signals(self, data):
        """Al/sat sinyalleri üretir"""
        data['Signal'] = 0
        data['Position'] = 0
        
        # Al sinyali: Close > SMA_5
        data.loc[data['Close'] > data['SMA_5'], 'Signal'] = 1
        # Sat sinyali: Close < SMA_5  
        data.loc[data['Close'] < data['SMA_5'], 'Signal'] = -1
        
        # Pozisyon değişimi
        data['Position'] = data['Signal'].diff()
        
        return data
    
    def backtest(self, data):
        """Backtesting işlemini gerçekleştirir"""
        print("🔄 Backtesting başlatılıyor...")
        
        self.capital = self.initial_capital
        shares = 0
        
        for i, row in data.iterrows():
            if pd.isna(row['SMA_5']):
                continue
                
            current_price = row['Close']
            signal = row['Signal']
            
            # Al sinyali
            if signal == 1 and shares == 0:
                shares = self.capital / current_price
                self.capital = 0
                self.trades.append({
                    'Date': row['Date'],
                    'Action': 'BUY',
                    'Price': current_price,
                    'Shares': shares
                })
                print(f"🟢 AL: {row['Date'].strftime('%Y-%m-%d')} - Fiyat: {current_price:.2f} TL")
            
            # Sat sinyali
            elif signal == -1 and shares > 0:
                self.capital = shares * current_price
                self.trades.append({
                    'Date': row['Date'],
                    'Action': 'SELL',
                    'Price': current_price,
                    'Shares': shares
                })
                print(f"🔴 SAT: {row['Date'].strftime('%Y-%m-%d')} - Fiyat: {current_price:.2f} TL")
                shares = 0
            
            # Portföy değeri hesaplama
            if shares > 0:
                portfolio_value = shares * current_price
            else:
                portfolio_value = self.capital
                
            self.portfolio_values.append(portfolio_value)
        
        # Son pozisyonu kapat
        if shares > 0:
            self.capital = shares * data['Close'].iloc[-1]
            self.trades.append({
                'Date': data['Date'].iloc[-1],
                'Action': 'SELL',
                'Price': data['Close'].iloc[-1],
                'Shares': shares
            })
            print(f"🔴 SON SAT: {data['Date'].iloc[-1].strftime('%Y-%m-%d')} - Fiyat: {data['Close'].iloc[-1]:.2f} TL")
        
        return {
            'final_capital': self.capital,
            'total_return': (self.capital - self.initial_capital) / self.initial_capital * 100,
            'trades': self.trades,
            'portfolio_values': self.portfolio_values
        }
    
    def plot_results(self, data, results):
        """Sonuçları görselleştirir"""
        print("📊 Grafikler oluşturuluyor...")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Hisse fiyatı ve hareketli ortalama
        ax1.plot(data['Date'], data['Close'], label='Hisse Fiyatı', linewidth=2, color='blue')
        ax1.plot(data['Date'], data['SMA_5'], label='5-Günlük MA', linewidth=2, color='orange')
        
        # Al/sat sinyalleri
        buy_signals = data[data['Position'] == 1]
        sell_signals = data[data['Position'] == -1]
        
        ax1.scatter(buy_signals['Date'], buy_signals['Close'], 
                   color='green', marker='^', s=100, label='Al Sinyali', zorder=5)
        ax1.scatter(sell_signals['Date'], sell_signals['Close'], 
                   color='red', marker='v', s=100, label='Sat Sinyali', zorder=5)
        
        ax1.set_title('Hisse Senedi Fiyatı ve Al/Sat Sinyalleri', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Fiyat (TL)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Portföy değeri
        portfolio_dates = data['Date'].iloc[:len(results['portfolio_values'])]
        ax2.plot(portfolio_dates, results['portfolio_values'], 
                color='purple', linewidth=2, label='Portföy Değeri')
        ax2.axhline(y=self.initial_capital, color='red', linestyle='--', 
                   label=f'Başlangıç Sermayesi ({self.initial_capital:,} TL)')
        
        ax2.set_title('Portföy Değeri Değişimi', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Tarih')
        ax2.set_ylabel('Portföy Değeri (TL)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, results):
        """Backtesting özetini yazdırır"""
        print("\n" + "="*60)
        print("📊 BACKTESTING SONUÇLARI")
        print("="*60)
        print(f"💰 Başlangıç Sermayesi: {self.initial_capital:,.2f} TL")
        print(f"💰 Final Sermaye: {results['final_capital']:,.2f} TL")
        print(f"📈 Toplam Getiri: {results['total_return']:.2f}%")
        print(f"🔄 Toplam İşlem Sayısı: {len(results['trades'])}")
        
        if results['trades']:
            print(f"📅 İlk İşlem: {results['trades'][0]['Date'].strftime('%Y-%m-%d')}")
            print(f"📅 Son İşlem: {results['trades'][-1]['Date'].strftime('%Y-%m-%d')}")
        
        # İşlem detayları
        if results['trades']:
            print("\n📋 İŞLEM DETAYLARI:")
            print("-" * 40)
            for trade in results['trades']:
                print(f"{trade['Date'].strftime('%Y-%m-%d')} | {trade['Action']} | "
                      f"Fiyat: {trade['Price']:.2f} TL | Adet: {trade['Shares']:.2f}")
        
        print("="*60)

def main():
    """Ana program fonksiyonu"""
    print("🤖 Hisse Senedi Alım-Satım Botu Başlatılıyor...")
    print("="*60)
    
    # Bot'u başlat
    bot = TradingBot(initial_capital=10000)
    
    # Örnek veri oluştur
    data = bot.create_sample_data()
    
    # Veriyi işle
    print("🔄 Hareketli ortalama hesaplanıyor...")
    data = bot.calculate_sma(data)
    
    print("🔄 Al/sat sinyalleri üretiliyor...")
    data = bot.generate_signals(data)
    
    # Backtesting yap
    results = bot.backtest(data)
    
    # Sonuçları göster
    bot.print_summary(results)
    bot.plot_results(data, results)
    
    print("\n✅ Program başarıyla tamamlandı!")
    print("📊 Grafikler açıldı. Kapatmak için pencereyi kapatın.")

if __name__ == "__main__":
    main()