"""
Streamlit Web Arayüzü
Hisse Senedi Alım-Satım Botu
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import yfinance as yf
import ta

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🤖 Hisse Senedi Alım-Satım Botu",
    page_icon="📈",
    layout="wide"
)

# Ana başlık
st.title("🤖 Hisse Senedi Alım-Satım Botu")
st.markdown("---")

# Sidebar - Parametreler
st.sidebar.header("⚙️ Bot Parametreleri")

# Hisse senedi seçimi
symbol = st.sidebar.text_input("Hisse Senedi Sembolü", value="AAPL", help="Örn: AAPL, TSLA, GOOGL")
period = st.sidebar.selectbox("Veri Periyodu", ["1y", "6mo", "3mo", "1mo"])

# Risk yönetimi
st.sidebar.subheader("🛡️ Risk Yönetimi")
stop_loss = st.sidebar.slider("Stop-Loss (%)", 1, 20, 5) / 100
take_profit = st.sidebar.slider("Take-Profit (%)", 5, 50, 10) / 100
initial_capital = st.sidebar.number_input("Başlangıç Sermayesi (TL)", 1000, 100000, 10000)

# Strateji parametreleri
st.sidebar.subheader("📊 Strateji Parametreleri")
sma_period = st.sidebar.slider("SMA Periyodu", 3, 50, 5)
rsi_period = st.sidebar.slider("RSI Periyodu", 5, 30, 14)

# Ana içerik
if st.button("🚀 Bot'u Başlat", type="primary"):
    
    with st.spinner("Veri çekiliyor ve analiz yapılıyor..."):
        
        # Veri çekme
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            data.reset_index(inplace=True)
            data.columns = [col.lower() for col in data.columns]
            
            st.success(f"✅ {symbol} için {len(data)} günlük veri çekildi")
            
        except Exception as e:
            st.error(f"❌ Veri çekme hatası: {e}")
            st.stop()
        
        # Teknik indikatörler
        data['sma'] = data['close'].rolling(window=sma_period).mean()
        data['rsi'] = ta.momentum.RSIIndicator(data['close'], window=rsi_period).rsi()
        
        # MACD
        macd = ta.trend.MACD(data['close'])
        data['macd'] = macd.macd()
        data['macd_signal'] = macd.macd_signal()
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(data['close'])
        data['bb_upper'] = bb.bollinger_hband()
        data['bb_lower'] = bb.bollinger_lband()
        
        # Sinyaller
        data['signal'] = 0
        data['position'] = 0
        
        for i in range(1, len(data)):
            if pd.isna(data['sma'].iloc[i]) or pd.isna(data['rsi'].iloc[i]):
                continue
                
            # Kombine sinyal
            sma_signal = 1 if data['close'].iloc[i] > data['sma'].iloc[i] else -1
            rsi_signal = 1 if data['rsi'].iloc[i] < 30 else (-1 if data['rsi'].iloc[i] > 70 else 0)
            macd_signal = 1 if data['macd'].iloc[i] > data['macd_signal'].iloc[i] else -1
            
            combined_signal = (sma_signal * 0.5 + rsi_signal * 0.3 + macd_signal * 0.2)
            
            if combined_signal > 0.3:
                data.loc[data.index[i], 'signal'] = 1
            elif combined_signal < -0.3:
                data.loc[data.index[i], 'signal'] = -1
        
        data['position'] = data['signal'].diff()
        
        # Backtesting
        capital = initial_capital
        shares = 0
        portfolio_values = []
        trades = []
        entry_price = 0
        
        for i, row in data.iterrows():
            if pd.isna(row['sma']):
                continue
                
            current_price = row['close']
            signal = row['signal']
            
            # Al sinyali
            if signal == 1 and shares == 0:
                shares = capital / current_price
                capital = 0
                entry_price = current_price
                trades.append({
                    'date': row['date'],
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares
                })
            
            # Sat sinyali
            elif signal == -1 and shares > 0:
                capital = shares * current_price
                trades.append({
                    'date': row['date'],
                    'action': 'SELL',
                    'price': current_price,
                    'shares': shares
                })
                shares = 0
            
            # Risk yönetimi
            elif shares > 0:
                # Stop-loss
                if current_price <= entry_price * (1 - stop_loss):
                    capital = shares * current_price
                    trades.append({
                        'date': row['date'],
                        'action': 'SELL',
                        'price': current_price,
                        'shares': shares,
                        'reason': 'Stop-Loss'
                    })
                    shares = 0
                # Take-profit
                elif current_price >= entry_price * (1 + take_profit):
                    capital = shares * current_price
                    trades.append({
                        'date': row['date'],
                        'action': 'SELL',
                        'price': current_price,
                        'shares': shares,
                        'reason': 'Take-Profit'
                    })
                    shares = 0
            
            # Portföy değeri
            portfolio_value = shares * current_price if shares > 0 else capital
            portfolio_values.append(portfolio_value)
        
        # Son pozisyonu kapat
        if shares > 0:
            capital = shares * data['close'].iloc[-1]
            trades.append({
                'date': data['date'].iloc[-1],
                'action': 'SELL',
                'price': data['close'].iloc[-1],
                'shares': shares,
                'reason': 'Final'
            })
        
        # Sonuçlar
        final_capital = capital
        total_return = (final_capital - initial_capital) / initial_capital * 100
        
        # Metrikler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Başlangıç", f"{initial_capital:,.0f} TL")
        
        with col2:
            st.metric("💰 Final", f"{final_capital:,.0f} TL")
        
        with col3:
            st.metric("📈 Getiri", f"{total_return:.2f}%")
        
        with col4:
            st.metric("🔄 İşlem Sayısı", len(trades))
        
        # Grafikler
        st.subheader("📊 Analiz Grafikleri")
        
        # 1. Hisse fiyatı ve sinyaller
        fig1 = go.Figure()
        
        # Fiyat çizgisi
        fig1.add_trace(go.Scatter(
            x=data['date'],
            y=data['close'],
            mode='lines',
            name='Hisse Fiyatı',
            line=dict(color='blue', width=2)
        ))
        
        # SMA
        fig1.add_trace(go.Scatter(
            x=data['date'],
            y=data['sma'],
            mode='lines',
            name=f'SMA {sma_period}',
            line=dict(color='orange', width=2)
        ))
        
        # Bollinger Bands
        fig1.add_trace(go.Scatter(
            x=data['date'],
            y=data['bb_upper'],
            mode='lines',
            name='BB Üst',
            line=dict(color='gray', dash='dash'),
            showlegend=False
        ))
        
        fig1.add_trace(go.Scatter(
            x=data['date'],
            y=data['bb_lower'],
            mode='lines',
            name='Bollinger Bands',
            line=dict(color='gray', dash='dash'),
            fill='tonexty'
        ))
        
        # Al/sat sinyalleri
        buy_signals = data[data['position'] == 1]
        sell_signals = data[data['position'] == -1]
        
        fig1.add_trace(go.Scatter(
            x=buy_signals['date'],
            y=buy_signals['close'],
            mode='markers',
            name='Al Sinyali',
            marker=dict(color='green', size=10, symbol='triangle-up')
        ))
        
        fig1.add_trace(go.Scatter(
            x=sell_signals['date'],
            y=sell_signals['close'],
            mode='markers',
            name='Sat Sinyali',
            marker=dict(color='red', size=10, symbol='triangle-down')
        ))
        
        fig1.update_layout(
            title=f'{symbol} Hisse Senedi Fiyatı ve Sinyaller',
            xaxis_title='Tarih',
            yaxis_title='Fiyat (TL)',
            height=500
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # 2. Portföy değeri
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=data['date'][:len(portfolio_values)],
            y=portfolio_values,
            mode='lines',
            name='Portföy Değeri',
            line=dict(color='purple', width=3)
        ))
        
        fig2.add_hline(
            y=initial_capital,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Başlangıç Sermayesi ({initial_capital:,} TL)"
        )
        
        fig2.update_layout(
            title='Portföy Değeri Değişimi',
            xaxis_title='Tarih',
            yaxis_title='Portföy Değeri (TL)',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # 3. RSI grafiği
        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatter(
            x=data['date'],
            y=data['rsi'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2)
        ))
        
        fig3.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
        fig3.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
        
        fig3.update_layout(
            title='RSI (Relative Strength Index)',
            xaxis_title='Tarih',
            yaxis_title='RSI',
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # İşlem detayları
        st.subheader("📋 İşlem Detayları")
        
        if trades:
            trades_df = pd.DataFrame(trades)
            st.dataframe(trades_df, use_container_width=True)
        else:
            st.info("Hiç işlem yapılmadı.")
        
        # İstatistikler
        st.subheader("📊 İstatistikler")
        
        if trades:
            buy_trades = [t for t in trades if t['action'] == 'BUY']
            sell_trades = [t for t in trades if t['action'] == 'SELL']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🟢 Al İşlemleri", len(buy_trades))
            
            with col2:
                st.metric("🔴 Sat İşlemleri", len(sell_trades))
            
            with col3:
                if len(trades) > 0:
                    first_trade = trades[0]['date']
                    last_trade = trades[-1]['date']
                    st.metric("📅 İşlem Süresi", f"{(last_trade - first_trade).days} gün")

# Footer
st.markdown("---")
st.markdown("🤖 **Hisse Senedi Alım-Satım Botu** - Gelişmiş analiz ve risk yönetimi")
st.markdown("⚠️ **Uyarı:** Bu bot sadece eğitim amaçlıdır. Gerçek yatırım yapmadan önce profesyonel danışmanlık alın.")