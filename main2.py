"""
Güncel Hisse Senedi Alım-Satım Botu
2025 başından şimdiye kadar güncel veri
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class CurrentTradingBot:
    def __init__(self, initial_capital=10000):
        """Güncel Trading Bot sınıfını başlatır"""
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.portfolio_values = []
        self.trades = []
        
    def get_current_data(self, symbol="AAPL", start_date="2025-01-01"):
        """
        2025 başından şimdiye kadar güncel veri çeker
        
        Args:
            symbol (str): Hisse senedi sembolü
            start_date (str): Başlangıç tarihi
            
        Returns:
            pd.DataFrame: Güncel hisse senedi verileri
        """
        print(f"📊 {symbol} için 2025 güncel veri çekiliyor...")
        print(f"📅 Tarih aralığı: {start_date} - {datetime.now().strftime('%Y-%m-%d')}")
        
        try:
            ticker = yf.Ticker(symbol)
            
            # Güncel veri çek
            data = ticker.history(
                start=start_date,
                end=datetime.now().strftime('%Y-%m-%d'),
                interval='1d'
            )
            
            if data.empty:
                print("❌ Veri bulunamadı, örnek veri oluşturuluyor...")
                return self.create_sample_data_2025()
            
            data.reset_index(inplace=True)
            data.columns = [col.lower() for col in data.columns]
            
            # Tarih formatını düzenle
            data['date'] = pd.to_datetime(data['date'])
            
            print(f"✅ {len(data)} günlük güncel veri çekildi")
            print(f"📈 İlk fiyat: {data['close'].iloc[0]:.2f} TL")
            print(f"📈 Son fiyat: {data['close'].iloc[-1]:.2f} TL")
            print(f"📊 Fiyat değişimi: {((data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0] * 100):.2f}%")
            
            return data
            
        except Exception as e:
            print(f"❌ Veri çekme hatası: {e}")
            print("📊 Örnek veri oluşturuluyor...")
            return self.create_sample_data_2025()
    
    def create_sample_data_2025(self):
        """2025 için örnek veri oluşturur"""
        print("📊 2025 örnek veri oluşturuluyor...")
        
        # 2025 başından bugüne kadar
        start_date = datetime(2025, 1, 1)
        end_date = datetime.now()
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Hafta sonları hariç (sadece iş günleri)
        dates = dates[dates.weekday < 5]
        
        np.random.seed(42)
        # 2025 için daha gerçekçi fiyat hareketi
        base_price = 100
        price_changes = np.random.randn(len(dates)) * 0.02  # %2 günlük volatilite
        prices = base_price * np.exp(np.cumsum(price_changes))
        
        data = pd.DataFrame({
            'date': dates,
            'close': prices,
            'high': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
            'low': prices * (1 - np.random.uniform(0, 0.02, len(dates))),
            'volume': np.random.randint(1000, 10000, len(dates))
        })
        
        print(f"✅ {len(data)} günlük 2025 örnek veri oluşturuldu")
        return data
    
    def get_multiple_stocks(self, symbols=["AAPL", "GOOGL", "MSFT", "TSLA"]):
        """
        Birden fazla hisse senedi verisi çeker
        
        Args:
            symbols (list): Hisse senedi sembolleri
            
        Returns:
            dict: Her hisse için veri
        """
        print("📊 Birden fazla hisse senedi verisi çekiliyor...")
        
        stocks_data = {}
        
        for symbol in symbols:
            print(f"\n🔄 {symbol} verisi çekiliyor...")
            try:
                data = self.get_current_data(symbol)
                stocks_data[symbol] = data
                print(f"✅ {symbol} verisi hazır")
            except Exception as e:
                print(f"❌ {symbol} veri çekme hatası: {e}")
        
        return stocks_data
    
    def calculate_technical_indicators(self, data):
        """Teknik indikatörleri hesaplar"""
        print("🔄 Teknik indikatörler hesaplanıyor...")
        
        # Hareketli ortalamalar
        data['sma_5'] = data['close'].rolling(window=5).mean()
        data['sma_10'] = data['close'].rolling(window=10).mean()
        data['sma_20'] = data['close'].rolling(window=20).mean()
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = data['close'].ewm(span=12).mean()
        exp2 = data['close'].ewm(span=26).mean()
        data['macd'] = exp1 - exp2
        data['macd_signal'] = data['macd'].ewm(span=9).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=20).mean()
        bb_std = data['close'].rolling(window=20).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * 2)
        data['bb_lower'] = data['bb_middle'] - (bb_std * 2)
        
        # Stochastic
        low_min = data['low'].rolling(window=14).min()
        high_max = data['high'].rolling(window=14).max()
        data['stoch_k'] = 100 * ((data['close'] - low_min) / (high_max - low_min))
        data['stoch_d'] = data['stoch_k'].rolling(window=3).mean()
        
        print("✅ Teknik indikatörler hesaplandı")
        return data
    
    def generate_signals(self, data):
        """Al/sat sinyalleri üretir"""
        print("🔄 Al/sat sinyalleri üretiliyor...")
        
        data['signal'] = 0
        data['position'] = 0
        
        for i in range(1, len(data)):
            if pd.isna(data['sma_5'].iloc[i]) or pd.isna(data['rsi'].iloc[i]):
                continue
                
            # Temel sinyal: SMA
            sma_signal = 1 if data['close'].iloc[i] > data['sma_5'].iloc[i] else -1
            
            # RSI sinyali
            rsi_signal = 0
            if data['rsi'].iloc[i] < 30:  # Oversold
                rsi_signal = 1
            elif data['rsi'].iloc[i] > 70:  # Overbought
                rsi_signal = -1
            
            # MACD sinyali
            macd_signal = 0
            if data['macd'].iloc[i] > data['macd_signal'].iloc[i]:
                macd_signal = 1
            elif data['macd'].iloc[i] < data['macd_signal'].iloc[i]:
                macd_signal = -1
            
            # Kombine sinyal
            combined_signal = (sma_signal * 0.5 + rsi_signal * 0.3 + macd_signal * 0.2)
            
            if combined_signal > 0.3:
                data.loc[data.index[i], 'signal'] = 1
            elif combined_signal < -0.3:
                data.loc[data.index[i], 'signal'] = -1
        
        # Pozisyon değişimi
        data['position'] = data['signal'].diff()
        
        # Sinyal sayıları
        buy_signals = len(data[data['position'] == 1])
        sell_signals = len(data[data['position'] == -1])
        
        print(f"✅ {buy_signals} al sinyali, {sell_signals} sat sinyali üretildi")
        return data
    
    def backtest(self, data):
        """Backtesting yapar"""
        print("🔄 2025 backtesting başlatılıyor...")
        
        self.capital = self.initial_capital
        shares = 0
        
        for i, row in data.iterrows():
            if pd.isna(row['sma_5']):
                continue
                
            current_price = row['close']
            signal = row['signal']
            
            # Al sinyali
            if signal == 1 and shares == 0:
                shares = self.capital / current_price
                self.capital = 0
                self.trades.append({
                    'date': row['date'],
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares
                })
                print(f"🟢 AL: {row['date'].strftime('%Y-%m-%d')} - Fiyat: {current_price:.2f} TL")
            
            # Sat sinyali
            elif signal == -1 and shares > 0:
                self.capital = shares * current_price
                self.trades.append({
                    'date': row['date'],
                    'action': 'SELL',
                    'price': current_price,
                    'shares': shares
                })
                print(f"🔴 SAT: {row['date'].strftime('%Y-%m-%d')} - Fiyat: {current_price:.2f} TL")
                shares = 0
            
            # Portföy değeri
            if shares > 0:
                portfolio_value = shares * current_price
            else:
                portfolio_value = self.capital
                
            self.portfolio_values.append(portfolio_value)
        
        # Son pozisyonu kapat
        if shares > 0:
            self.capital = shares * data['close'].iloc[-1]
            self.trades.append({
                'date': data['date'].iloc[-1],
                'action': 'SELL',
                'price': data['close'].iloc[-1],
                'shares': shares
            })
            print(f"🔴 SON SAT: {data['date'].iloc[-1].strftime('%Y-%m-%d')} - Fiyat: {data['close'].iloc[-1]:.2f} TL")
        
        return {
            'final_capital': self.capital,
            'total_return': (self.capital - self.initial_capital) / self.initial_capital * 100,
            'trades': self.trades,
            'portfolio_values': self.portfolio_values
        }
    
    def plot_current_results(self, data, results):
        """Güncel sonuçları görselleştirir"""
        print("📊 2025 güncel grafikler oluşturuluyor...")
        
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))
        
        # 1. Hisse fiyatı ve sinyaller
        ax1 = axes[0]
        ax1.plot(data['date'], data['close'], label='Hisse Fiyatı', linewidth=2, color='blue')
        ax1.plot(data['date'], data['sma_5'], label='5-Günlük MA', linewidth=2, color='orange')
        ax1.plot(data['date'], data['sma_20'], label='20-Günlük MA', linewidth=2, color='red')
        
        # Bollinger Bands
        ax1.fill_between(data['date'], data['bb_upper'], data['bb_lower'], 
                        alpha=0.2, color='gray', label='Bollinger Bands')
        
        # Al/sat sinyalleri
        buy_signals = data[data['position'] == 1]
        sell_signals = data[data['position'] == -1]
        
        ax1.scatter(buy_signals['date'], buy_signals['close'], 
                   color='green', marker='^', s=100, label='Al Sinyali', zorder=5)
        ax1.scatter(sell_signals['date'], sell_signals['close'], 
                   color='red', marker='v', s=100, label='Sat Sinyali', zorder=5)
        
        ax1.set_title('2025 Güncel Hisse Senedi Fiyatı ve Sinyaller', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Fiyat (TL)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. RSI
        ax2 = axes[1]
        ax2.plot(data['date'], data['rsi'], label='RSI', color='purple', linewidth=2)
        ax2.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax2.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax2.set_ylabel('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Portföy değeri
        ax3 = axes[2]
        portfolio_dates = data['date'].iloc[:len(results['portfolio_values'])]
        ax3.plot(portfolio_dates, results['portfolio_values'], 
                color='purple', linewidth=2, label='Portföy Değeri')
        ax3.axhline(y=self.initial_capital, color='red', linestyle='--', 
                   label=f'Başlangıç Sermayesi ({self.initial_capital:,} TL)')
        
        ax3.set_title('2025 Portföy Değeri Değişimi', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Tarih')
        ax3.set_ylabel('Portföy Değeri (TL)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def print_current_summary(self, results):
        """Güncel backtesting özetini yazdırır"""
        print("\n" + "="*70)
        print("📊 2025 GÜNCEL BACKTESTING SONUÇLARI")
        print("="*70)
        print(f"💰 Başlangıç Sermayesi: {self.initial_capital:,.2f} TL")
        print(f"💰 Final Sermaye: {results['final_capital']:,.2f} TL")
        print(f"📈 Toplam Getiri: {results['total_return']:.2f}%")
        print(f"🔄 Toplam İşlem Sayısı: {len(results['trades'])}")
        
        if results['trades']:
            print(f"📅 İlk İşlem: {results['trades'][0]['date'].strftime('%Y-%m-%d')}")
            print(f"📅 Son İşlem: {results['trades'][-1]['date'].strftime('%Y-%m-%d')}")
        
        # İşlem detayları
        if results['trades']:
            print("\n📋 2025 İŞLEM DETAYLARI:")
            print("-" * 60)
            for trade in results['trades']:
                print(f"{trade['date'].strftime('%Y-%m-%d')} | {trade['action']} | "
                      f"Fiyat: {trade['price']:.2f} TL | Adet: {trade['shares']:.2f}")
        
        print("="*70)

def main():
    """Ana program fonksiyonu"""
    print("🤖 2025 Güncel Hisse Senedi Alım-Satım Botu Başlatılıyor...")
    print("="*70)
    
    # Bot'u başlat
    bot = CurrentTradingBot(initial_capital=10000)
    
    # Hisse senedi seçimi
    print("📊 Hangi hisse senedi için analiz yapmak istiyorsunuz?")
    print("1. AAPL (Apple)")
    print("2. GOOGL (Google)")
    print("3. MSFT (Microsoft)")
    print("4. TSLA (Tesla)")
    print("5. Özel sembol girin")
    
    choice = input("Seçiminiz (1-5): ").strip()
    
    symbol_map = {
        '1': 'AAPL',
        '2': 'GOOGL', 
        '3': 'MSFT',
        '4': 'TSLA'
    }
    
    if choice in symbol_map:
        symbol = symbol_map[choice]
    elif choice == '5':
        symbol = input("Hisse senedi sembolü girin (örn: AAPL): ").upper()
    else:
        symbol = 'AAPL'
        print("Varsayılan olarak AAPL seçildi")
    
    print(f"\n🔄 {symbol} için 2025 güncel veri çekiliyor...")
    
    # Güncel veri çek
    data = bot.get_current_data(symbol, start_date="2025-01-01")
    
    # Teknik indikatörleri hesapla
    data = bot.calculate_technical_indicators(data)
    
    # Sinyaller üret
    data = bot.generate_signals(data)
    
    # Backtesting yap
    results = bot.backtest(data)
    
    # Sonuçları göster
    bot.print_current_summary(results)
    bot.plot_current_results(data, results)
    
    print("\n✅ 2025 güncel program başarıyla tamamlandı!")
    print("📊 Grafikler açıldı. Kapatmak için pencereyi kapatın.")

if __name__ == "__main__":
    main()