"""
Marketing Mix Modeling - Data Generation (Python Version)
Author: Shruthi
Purpose: Generate realistic e-commerce marketing data for portfolio
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Parameters
n_weeks = 156  # 3 years of weekly data (2021-2023)

# ============================================================================
# 1. TIME VARIABLES
# ============================================================================

# Create date sequence
start_date = datetime(2021, 1, 1)
dates = [start_date + timedelta(weeks=i) for i in range(n_weeks)]
week_num = np.arange(1, n_weeks + 1)

# Extract time features
months = np.array([d.month for d in dates])
quarters = np.ceil(months / 3).astype(int)
years = np.array([d.year for d in dates])

# Holiday indicators
# Black Friday (week 47), Cyber Monday (week 48), Christmas (weeks 51-52)
black_friday_weeks = [47, 99, 151]
cyber_monday_weeks = [48, 100, 152]
christmas_weeks = [51, 52, 103, 104, 155, 156]
new_year_weeks = [1, 53, 105]

holiday_weeks = set(black_friday_weeks + cyber_monday_weeks + christmas_weeks + new_year_weeks)
holiday = np.array([1 if w in holiday_weeks else 0 for w in week_num])

# Q4 indicator (holiday season)
q4 = (quarters == 4).astype(int)

# ============================================================================
# 2. MARKETING SPEND VARIABLES (with realistic patterns)
# ============================================================================

# Base seasonal pattern (higher in Q4)
seasonal_multiplier = 1 + 0.3 * q4 + 0.1 * (quarters == 1)

# TV Advertising (weekly spend in $1000s)
tv_base = np.random.normal(15, 3, n_weeks)
tv_spend = np.maximum(2, tv_base * seasonal_multiplier + holiday * np.random.normal(5, 1, n_weeks))

# Digital Advertising (weekly spend in $1000s)
digital_base = np.random.normal(20, 5, n_weeks)
digital_spend = np.maximum(3, digital_base * seasonal_multiplier + holiday * np.random.normal(8, 2, n_weeks))

# Social Media (weekly spend in $1000s) - growing over time
social_base = 5 + 0.05 * week_num + np.random.normal(0, 2, n_weeks)
social_spend = np.maximum(1, social_base * seasonal_multiplier + holiday * np.random.normal(10, 2, n_weeks))

# Email Marketing (weekly spend in $1000s)
email_base = np.random.normal(3, 0.8, n_weeks)
email_spend = np.maximum(0.5, email_base + holiday * np.random.normal(2, 0.5, n_weeks))

# Search/SEM (weekly spend in $1000s)
sem_base = np.random.normal(12, 2.5, n_weeks)
sem_spend = np.maximum(2, sem_base * 1.1 * seasonal_multiplier + holiday * np.random.normal(5, 1, n_weeks))

# Promotions/Discounts (binary)
promo_prob = 0.15 + 0.25 * q4
promotion = np.random.binomial(1, promo_prob, n_weeks)

# ============================================================================
# 3. EXTERNAL FACTORS
# ============================================================================

# Competitor activity (index: 0-100)
competitor_index = 50 + np.random.normal(0, 10, n_weeks)
competitor_index = np.clip(competitor_index, 20, 80)

# Economic indicator (consumer confidence index: 0-150)
economic_index = 100 + 0.03 * week_num + np.random.normal(0, 5, n_weeks)
economic_index = np.clip(economic_index, 80, 120)

# ============================================================================
# 4. GENERATE SALES (Dependent Variable)
# ============================================================================

# True model parameters
beta_0 = 4.5
beta_tv = 0.08
beta_digital = 0.12
beta_social = 0.10
beta_email = 0.06
beta_sem = 0.09
beta_promo = 0.15
beta_holiday = 0.20
beta_competitor = -0.003
beta_economic = 0.004
beta_lag = 0.30

# Initialize sales
log_sales = np.zeros(n_weeks)

# Generate first week
log_sales[0] = (beta_0 + 
                beta_tv * np.log(tv_spend[0]) +
                beta_digital * np.log(digital_spend[0]) +
                beta_social * np.log(social_spend[0]) +
                beta_email * np.log(email_spend[0]) +
                beta_sem * np.log(sem_spend[0]) +
                beta_promo * promotion[0] +
                beta_holiday * holiday[0] +
                beta_competitor * competitor_index[0] +
                beta_economic * economic_index[0] +
                np.random.normal(0, 0.08))

# Generate remaining weeks with lagged effect
for i in range(1, n_weeks):
    log_sales[i] = (beta_0 + 
                    beta_lag * log_sales[i-1] +
                    beta_tv * np.log(tv_spend[i]) +
                    beta_digital * np.log(digital_spend[i]) +
                    beta_social * np.log(social_spend[i]) +
                    beta_email * np.log(email_spend[i]) +
                    beta_sem * np.log(sem_spend[i]) +
                    beta_promo * promotion[i] +
                    beta_holiday * holiday[i] +
                    beta_competitor * competitor_index[i] +
                    beta_economic * economic_index[i] +
                    np.random.normal(0, 0.08))

# Convert to actual sales
sales = np.exp(log_sales)

# Add interaction effect: Digital works better during holidays
holiday_digital_boost = np.where(holiday == 1, 0.15 * np.log(digital_spend), 0)
sales = sales * np.exp(holiday_digital_boost)

# ============================================================================
# 5. CREATE DATAFRAME
# ============================================================================

marketing_data = pd.DataFrame({
    'week': week_num,
    'date': dates,
    'year': years,
    'quarter': quarters,
    'month': months,
    'sales': np.round(sales, 2),
    'tv_spend': np.round(tv_spend, 2),
    'digital_spend': np.round(digital_spend, 2),
    'social_spend': np.round(social_spend, 2),
    'email_spend': np.round(email_spend, 2),
    'sem_spend': np.round(sem_spend, 2),
    'promotion': promotion,
    'holiday': holiday,
    'competitor_index': np.round(competitor_index, 1),
    'economic_index': np.round(economic_index, 1)
})

# ============================================================================
# 6. SAVE DATA
# ============================================================================

marketing_data.to_csv('marketing_mix_data.csv', index=False)

print("=" * 60)
print("Marketing Mix Data Generated Successfully!")
print("=" * 60)
print(f"\nDataset Dimensions: {marketing_data.shape[0]} weeks × {marketing_data.shape[1]} variables")
print(f"\nDate Range: {marketing_data['date'].min()} to {marketing_data['date'].max()}")
print(f"Total Sales: ${marketing_data['sales'].sum():,.0f}K")
print(f"Average Weekly Sales: ${marketing_data['sales'].mean():,.0f}K")

print("\n" + "=" * 60)
print("Summary Statistics:")
print("=" * 60)
print(marketing_data[['sales', 'tv_spend', 'digital_spend', 'social_spend', 
                       'email_spend', 'sem_spend']].describe().round(2))

print("\n" + "=" * 60)
print("First 10 rows:")
print("=" * 60)
print(marketing_data.head(10))

print("\n" + "=" * 60)
print("Holiday weeks sample:")
print("=" * 60)
print(marketing_data[marketing_data['holiday'] == 1].head(5))

print("\nData saved to: marketing_mix_data.csv")
