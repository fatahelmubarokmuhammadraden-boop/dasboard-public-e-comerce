import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: white;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data Function
@st.cache_data
def load_data():
    """Load and preprocess bike sharing data"""
    try:
        # Try to load from day.csv (relative path for deployment)
        day_df = pd.read_csv('day.csv')
        hour_df = pd.read_csv('hour.csv')
        
        # Convert date column
        day_df['dteday'] = pd.to_datetime(day_df['dteday'])
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
        
        # Add readable labels
        season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
        weather_map = {
            1: 'Clear', 
            2: 'Mist/Cloudy', 
            3: 'Light Rain/Snow', 
            4: 'Heavy Rain/Snow'
        }
        month_map = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        weekday_map = {
            0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed',
            4: 'Thu', 5: 'Fri', 6: 'Sat'
        }
        
        day_df['season_name'] = day_df['season'].map(season_map)
        day_df['weather_name'] = day_df['weathersit'].map(weather_map)
        day_df['month_name'] = day_df['mnth'].map(month_map)
        day_df['weekday_name'] = day_df['weekday'].map(weekday_map)
        day_df['year'] = day_df['yr'].map({0: '2011', 1: '2012'})
        
        hour_df['season_name'] = hour_df['season'].map(season_map)
        hour_df['weather_name'] = hour_df['weathersit'].map(weather_map)
        
        # Denormalize temperature and other metrics
        day_df['temp_celsius'] = day_df['temp'] * 41
        day_df['atemp_celsius'] = day_df['atemp'] * 50
        day_df['humidity_pct'] = day_df['hum'] * 100
        day_df['windspeed_kmh'] = day_df['windspeed'] * 67
        
        hour_df['temp_celsius'] = hour_df['temp'] * 41
        hour_df['humidity_pct'] = hour_df['hum'] * 100
        hour_df['windspeed_kmh'] = hour_df['windspeed'] * 67
        
        return day_df, hour_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Statistical Analysis Functions
def perform_statistical_analysis(df):
    """Perform comprehensive statistical analysis"""
    stats = {
        'total_rides': df['cnt'].sum(),
        'avg_daily_rides': df['cnt'].mean(),
        'median_rides': df['cnt'].median(),
        'std_rides': df['cnt'].std(),
        'max_rides': df['cnt'].max(),
        'min_rides': df['cnt'].min(),
        'total_casual': df['casual'].sum(),
        'total_registered': df['registered'].sum(),
        'avg_temp': df['temp_celsius'].mean(),
        'avg_humidity': df['humidity_pct'].mean(),
        'avg_windspeed': df['windspeed_kmh'].mean()
    }
    return stats

def correlation_analysis(df):
    """Analyze correlations between variables"""
    numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    correlation_matrix = df[numeric_cols].corr()
    return correlation_matrix

# Load data
st.title("🚴 Dashboard Analisis Bike Sharing")
st.markdown("### Analisis Komprehensif Data Penyewaan Sepeda Washington D.C. (2011-2012)")

with st.spinner("Memuat data..."):
    day_df, hour_df = load_data()

if day_df is not None and hour_df is not None:
    
    # Sidebar untuk filter
    st.sidebar.header("🎛️ Filter Data")
    
    # Year filter
    selected_year = st.sidebar.multiselect(
        "Pilih Tahun",
        options=day_df['year'].unique(),
        default=day_df['year'].unique()
    )
    
    # Season filter
    selected_season = st.sidebar.multiselect(
        "Pilih Musim",
        options=day_df['season_name'].unique(),
        default=day_df['season_name'].unique()
    )
    
    # Filter data
    filtered_df = day_df[
        (day_df['year'].isin(selected_year)) &
        (day_df['season_name'].isin(selected_season))
    ]
    
    # Calculate statistics
    stats = perform_statistical_analysis(filtered_df)
    
    # === SECTION 1: Key Metrics ===
    st.markdown("---")
    st.header("📊 Metrik Utama")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Penyewaan",
            value=f"{stats['total_rides']:,.0f}",
            delta="🚴"
        )
    
    with col2:
        st.metric(
            label="Rata-rata Harian",
            value=f"{stats['avg_daily_rides']:,.0f}",
            delta=f"±{stats['std_rides']:,.0f}"
        )
    
    with col3:
        st.metric(
            label="Suhu Rata-rata",
            value=f"{stats['avg_temp']:.1f}°C",
            delta="🌡️"
        )
    
    with col4:
        st.metric(
            label="Kelembaban Rata-rata",
            value=f"{stats['avg_humidity']:.1f}%",
            delta="💧"
        )
    
    # === SECTION 2: User Type Analysis ===
    st.markdown("---")
    st.header("👥 Analisis Tipe Pengguna")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for user types
        fig, ax = plt.subplots(figsize=(8, 6))
        user_data = [stats['total_casual'], stats['total_registered']]
        colors = ['#FF6B6B', '#4ECDC4']
        explode = (0.05, 0.05)
        
        ax.pie(user_data, labels=['Casual', 'Registered'], autopct='%1.1f%%',
               colors=colors, explode=explode, shadow=True, startangle=90)
        ax.set_title('Distribusi Tipe Pengguna', fontsize=14, fontweight='bold')
        st.pyplot(fig)
        plt.close()
        
        # Show numbers
        st.info(f"""
        **Casual Users**: {stats['total_casual']:,.0f} ({stats['total_casual']/stats['total_rides']*100:.1f}%)
        
        **Registered Users**: {stats['total_registered']:,.0f} ({stats['total_registered']/stats['total_rides']*100:.1f}%)
        """)
    
    with col2:
        # Bar chart comparison by month
        monthly_users = filtered_df.groupby('month_name')[['casual', 'registered']].mean().reindex(
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(monthly_users.index))
        width = 0.35
        
        ax.bar(x - width/2, monthly_users['casual'], width, label='Casual', color='#FF6B6B')
        ax.bar(x + width/2, monthly_users['registered'], width, label='Registered', color='#4ECDC4')
        
        ax.set_xlabel('Bulan', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax.set_title('Perbandingan Tipe Pengguna per Bulan', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(monthly_users.index, rotation=45)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # === SECTION 3: Temporal Analysis ===
    st.markdown("---")
    st.header("📅 Analisis Temporal")
    
    tab1, tab2, tab3 = st.tabs(["Tren Bulanan", "Pola Musiman", "Pola Mingguan"])
    
    with tab1:
        # Monthly trend with both years
        fig, ax = plt.subplots(figsize=(14, 6))
        
        for year in filtered_df['year'].unique():
            year_data = filtered_df[filtered_df['year'] == year]
            monthly_avg = year_data.groupby('mnth')['cnt'].mean()
            ax.plot(monthly_avg.index, monthly_avg.values, marker='o', 
                   linewidth=2, label=f'Tahun {year}', markersize=8)
        
        ax.set_xlabel('Bulan', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan per Hari', fontsize=12)
        ax.set_title('Tren Penyewaan Bulanan', fontsize=14, fontweight='bold')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Statistical insight
        peak_month = filtered_df.groupby('month_name')['cnt'].mean().idxmax()
        peak_value = filtered_df.groupby('month_name')['cnt'].mean().max()
        st.success(f"📈 **Peak Month**: {peak_month} dengan rata-rata {peak_value:,.0f} penyewaan per hari")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Seasonal distribution
            seasonal_data = filtered_df.groupby('season_name')['cnt'].sum()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors_season = ['#A8DADC', '#457B9D', '#E63946', '#F4A261']
            wedges, texts, autotexts = ax.pie(seasonal_data.values, labels=seasonal_data.index, 
                                               autopct='%1.1f%%', colors=colors_season,
                                               explode=[0.05]*len(seasonal_data), shadow=True,
                                               startangle=90)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title('Distribusi Penyewaan per Musim', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        with col2:
            # Box plot by season
            fig, ax = plt.subplots(figsize=(8, 6))
            season_order = ['Winter', 'Spring', 'Summer', 'Fall']
            filtered_season = filtered_df[filtered_df['season_name'].isin(season_order)]
            
            bp = ax.boxplot([filtered_season[filtered_season['season_name'] == s]['cnt'].values 
                            for s in season_order],
                           labels=season_order, patch_artist=True)
            
            for patch, color in zip(bp['boxes'], colors_season):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
            ax.set_title('Distribusi Penyewaan per Musim', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
    
    with tab3:
        # Weekday vs Weekend comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # By weekday
        weekday_avg = filtered_df.groupby('weekday_name')['cnt'].mean().reindex(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        )
        
        colors_week = ['#FF6B6B' if day in ['Sat', 'Sun'] else '#4ECDC4' 
                      for day in weekday_avg.index]
        
        ax1.bar(weekday_avg.index, weekday_avg.values, color=colors_week)
        ax1.set_xlabel('Hari dalam Seminggu', fontsize=12)
        ax1.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax1.set_title('Pola Penyewaan per Hari', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Working day vs non-working day
        workday_comparison = filtered_df.groupby('workingday')['cnt'].mean()
        
        ax2.bar(['Non-Working Day', 'Working Day'], 
               [workday_comparison[0], workday_comparison[1]],
               color=['#FF6B6B', '#4ECDC4'])
        ax2.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax2.set_title('Working Day vs Non-Working Day', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # === SECTION 4: Weather Impact Analysis ===
    st.markdown("---")
    st.header("🌤️ Analisis Dampak Cuaca")
    
    tab1, tab2 = st.tabs(["Kondisi Cuaca", "Korelasi"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Weather situation impact
            weather_avg = filtered_df.groupby('weather_name')['cnt'].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors_weather = ['#52B788', '#74C69D', '#95D5B2', '#B7E4C7']
            ax.barh(weather_avg.index, weather_avg.values, color=colors_weather)
            ax.set_xlabel('Rata-rata Penyewaan', fontsize=12)
            ax.set_title('Dampak Kondisi Cuaca', fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, v in enumerate(weather_avg.values):
                ax.text(v + 50, i, f'{v:.0f}', va='center', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            # Temperature impact
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Create temperature bins
            temp_bins = pd.cut(filtered_df['temp_celsius'], bins=5)
            temp_impact = filtered_df.groupby(temp_bins)['cnt'].mean()
            
            ax.plot(range(len(temp_impact)), temp_impact.values, marker='o', 
                   linewidth=2, markersize=10, color='#E63946')
            ax.fill_between(range(len(temp_impact)), temp_impact.values, alpha=0.3, color='#E63946')
            
            ax.set_xlabel('Rentang Suhu', fontsize=12)
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
            ax.set_title('Dampak Suhu terhadap Penyewaan', fontsize=14, fontweight='bold')
            ax.set_xticks(range(len(temp_impact)))
            ax.set_xticklabels([f'{int(i.left)}-{int(i.right)}°C' 
                               for i in temp_impact.index], rotation=45)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
    
    with tab2:
        # Correlation heatmap
        corr_matrix = correlation_analysis(filtered_df)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax)
        ax.set_title('Matriks Korelasi Variabel', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Correlation insights
        st.info("""
        **📊 Insight Korelasi:**
        - Temperature (temp/atemp) memiliki korelasi positif kuat dengan jumlah penyewaan
        - Humidity memiliki korelasi negatif dengan penyewaan
        - Registered users mendominasi total penyewaan
        """)
    
    # === SECTION 5: Hourly Pattern Analysis ===
    st.markdown("---")
    st.header("⏰ Analisis Pola Jam (Hour Data)")
    
    # Filter hour data
    filtered_hour = hour_df[
        (hour_df['yr'].map({0: '2011', 1: '2012'}).isin(selected_year))
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly pattern
        hourly_avg = filtered_hour.groupby('hr')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(hourly_avg.index, hourly_avg.values, marker='o', 
               linewidth=2, markersize=8, color='#457B9D')
        ax.fill_between(hourly_avg.index, hourly_avg.values, alpha=0.3, color='#457B9D')
        
        ax.set_xlabel('Jam (0-23)', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax.set_title('Pola Penyewaan per Jam', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(0, 24, 2))
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        peak_hour = hourly_avg.idxmax()
        st.success(f"🕐 **Peak Hour**: {peak_hour}:00 dengan rata-rata {hourly_avg[peak_hour]:.0f} penyewaan")
    
    with col2:
        # Heatmap: Hour vs Weekday
        hourly_weekday = filtered_hour.pivot_table(
            values='cnt', 
            index='hr', 
            columns='weekday', 
            aggfunc='mean'
        )
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(hourly_weekday, cmap='YlOrRd', annot=False, 
                   fmt='.0f', cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_xlabel('Hari (0=Sun, 6=Sat)', fontsize=12)
        ax.set_ylabel('Jam', fontsize=12)
        ax.set_title('Heatmap: Penyewaan per Jam dan Hari', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # === SECTION 6: Download & Raw Data ===
    st.markdown("---")
    st.header("📁 Data & Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Preview Data Harian")
        st.dataframe(filtered_df[['dteday', 'season_name', 'weather_name', 
                                  'temp_celsius', 'humidity_pct', 'casual', 
                                  'registered', 'cnt']].head(10))
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data Harian (CSV)",
            data=csv,
            file_name="bike_sharing_daily.csv",
            mime="text/csv"
        )
    
    with col2:
        st.subheader("Statistik Deskriptif")
        st.dataframe(filtered_df[['temp_celsius', 'humidity_pct', 'windspeed_kmh', 
                                  'casual', 'registered', 'cnt']].describe())
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: white;'>
        <p>📊 Dashboard dibuat dengan Streamlit | Data: Capital Bikeshare, Washington D.C.</p>
        <p>🔍 Analisis menggunakan: Pandas, NumPy, Matplotlib, Seaborn</p>
    </div>
    """, unsafe_allow_html=True)
    
else:
    st.error("❌ Gagal memuat data. Pastikan file day.csv dan hour.csv tersedia.")
