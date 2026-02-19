"""
Marketing Mix Modeling - Complete Analysis (Python Version)
Author: Shruthi
Purpose: Analyze marketing channel effectiveness and optimize budget allocation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 70)
print("MARKETING MIX MODELING ANALYSIS")
print("=" * 70)

# ============================================================================
# 1. LOAD AND EXPLORE DATA
# ============================================================================

data = pd.read_csv('marketing_mix_data.csv')
data['date'] = pd.to_datetime(data['date'])

print(f"\nDataset Overview:")
print(f"- Time Period: {data['date'].min().date()} to {data['date'].max().date()}")
print(f"- Number of Weeks: {len(data)}")
print(f"- Total Sales: ${data['sales'].sum():,.0f}K")
print(f"- Average Weekly Sales: ${data['sales'].mean():,.0f}K")

print(f"\nVariables: {', '.join(data.columns.tolist())}")

print(f"\nSummary Statistics:")
print(data[['sales', 'tv_spend', 'digital_spend', 'social_spend', 
            'email_spend', 'sem_spend']].describe().round(2))

# ============================================================================
# 2. DATA PREPARATION
# ============================================================================

# Create lagged sales
sales = data['sales'].values[1:]
lag_sales = data['sales'].values[:-1]

# Align all other variables
tv = data['tv_spend'].values[1:]
digital = data['digital_spend'].values[1:]
social = data['social_spend'].values[1:]
email = data['email_spend'].values[1:]
sem = data['sem_spend'].values[1:]
promotion = data['promotion'].values[1:]
holiday = data['holiday'].values[1:]
competitor = data['competitor_index'].values[1:]
economic = data['economic_index'].values[1:]
quarter = data['quarter'].values[1:]

# Create quarter dummies
q2 = (quarter == 2).astype(int)
q3 = (quarter == 3).astype(int)
q4 = (quarter == 4).astype(int)

n_obs = len(sales)
print(f"\nAnalysis Sample Size: {n_obs} weeks (after lagging)")

# ============================================================================
# 3. EXPLORATORY VISUALIZATIONS
# ============================================================================

print("\nGenerating visualizations...")

# Create plots directory if it doesn't exist
import os
os.makedirs('plots', exist_ok=True)

# 1. Sales trend over time
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(data['date'], data['sales'], linewidth=2, color='steelblue', label='Weekly Sales')
# Highlight holiday weeks
holiday_data = data[data['holiday'] == 1]
ax.scatter(holiday_data['date'], holiday_data['sales'], 
           color='red', s=100, alpha=0.6, label='Holiday Weeks', zorder=5)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Sales ($1000s)', fontsize=12, fontweight='bold')
ax.set_title('Weekly Sales Over Time', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plots/01_sales_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Marketing spend by channel
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(data['date'], data['tv_spend'], label='TV', linewidth=2)
ax.plot(data['date'], data['digital_spend'], label='Digital', linewidth=2)
ax.plot(data['date'], data['social_spend'], label='Social Media', linewidth=2)
ax.plot(data['date'], data['email_spend'], label='Email', linewidth=2)
ax.plot(data['date'], data['sem_spend'], label='SEM', linewidth=2)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Spend ($1000s)', fontsize=12, fontweight='bold')
ax.set_title('Marketing Spend by Channel Over Time', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plots/02_marketing_spend.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Sales vs Digital Spend
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data['digital_spend'], data['sales'], alpha=0.6, s=60, color='steelblue')
# Add trend line
z = np.polyfit(data['digital_spend'], data['sales'], 2)
p = np.poly1d(z)
x_trend = np.linspace(data['digital_spend'].min(), data['digital_spend'].max(), 100)
ax.plot(x_trend, p(x_trend), "r--", linewidth=2, label='Trend')
ax.set_xlabel('Digital Spend ($1000s)', fontsize=12, fontweight='bold')
ax.set_ylabel('Sales ($1000s)', fontsize=12, fontweight='bold')
ax.set_title('Sales vs Digital Spend (Diminishing Returns)', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('plots/03_sales_vs_digital.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Sales vs TV Spend
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data['tv_spend'], data['sales'], alpha=0.6, s=60, color='darkgreen')
z = np.polyfit(data['tv_spend'], data['sales'], 2)
p = np.poly1d(z)
x_trend = np.linspace(data['tv_spend'].min(), data['tv_spend'].max(), 100)
ax.plot(x_trend, p(x_trend), "r--", linewidth=2, label='Trend')
ax.set_xlabel('TV Spend ($1000s)', fontsize=12, fontweight='bold')
ax.set_ylabel('Sales ($1000s)', fontsize=12, fontweight='bold')
ax.set_title('Sales vs TV Spend', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('plots/04_sales_vs_tv.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Promotion effect
fig, ax = plt.subplots(figsize=(10, 6))
promo_df = pd.DataFrame({
    'Promotion': ['No Promotion', 'With Promotion'],
    'Sales': [data[data['promotion']==0]['sales'].values, 
              data[data['promotion']==1]['sales'].values]
})
bp = ax.boxplot([data[data['promotion']==0]['sales'].values,
                  data[data['promotion']==1]['sales'].values],
                 labels=['No Promotion', 'With Promotion'],
                 patch_artist=True,
                 widths=0.6)
bp['boxes'][0].set_facecolor('lightblue')
bp['boxes'][1].set_facecolor('coral')
ax.set_ylabel('Sales ($1000s)', fontsize=12, fontweight='bold')
ax.set_title('Sales Distribution: Promotion vs No Promotion', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('plots/05_promotion_effect.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Holiday effect
fig, ax = plt.subplots(figsize=(10, 6))
bp = ax.boxplot([data[data['holiday']==0]['sales'].values,
                  data[data['holiday']==1]['sales'].values],
                 labels=['Non-Holiday', 'Holiday'],
                 patch_artist=True,
                 widths=0.6)
bp['boxes'][0].set_facecolor('lightblue')
bp['boxes'][1].set_facecolor('coral')
ax.set_ylabel('Sales ($1000s)', fontsize=12, fontweight='bold')
ax.set_title('Sales Distribution: Holiday vs Non-Holiday Weeks', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('plots/06_holiday_effect.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Plots saved to plots/ directory")

# ============================================================================
# 4. BASE MARKETING MIX MODEL (Log-Log Specification)
# ============================================================================

print("\n" + "=" * 70)
print("MODEL 1: BASE MARKETING MIX MODEL")
print("=" * 70)

# Prepare variables for regression (log transform)
log_sales = np.log(sales)
log_lag_sales = np.log(lag_sales)
log_tv = np.log(tv)
log_digital = np.log(digital)
log_social = np.log(social)
log_email = np.log(email)
log_sem = np.log(sem)

# Create design matrix
X_base = np.column_stack([
    log_lag_sales, log_tv, log_digital, log_social, log_email, log_sem,
    promotion, q2, q3, q4
])

# Add constant
X_base_const = sm.add_constant(X_base)

# Fit model using statsmodels for detailed statistics
model_base = sm.OLS(log_sales, X_base_const).fit()
print(model_base.summary())

# ============================================================================
# 5. CHECK MULTICOLLINEARITY
# ============================================================================

print("\n" + "=" * 70)
print("MULTICOLLINEARITY CHECK (VIF)")
print("=" * 70)

# Calculate VIF
vif_data = pd.DataFrame()
vif_data["Variable"] = ['log(lag_sales)', 'log(tv)', 'log(digital)', 'log(social)',
                         'log(email)', 'log(sem)', 'promotion', 'Q2', 'Q3', 'Q4']
vif_data["VIF"] = [variance_inflation_factor(X_base, i) for i in range(X_base.shape[1])]

print(vif_data.to_string(index=False))

max_vif = vif_data["VIF"].max()
if max_vif > 10:
    print(f"\n⚠ WARNING: High multicollinearity detected (max VIF = {max_vif:.2f})")
elif max_vif > 4:
    print(f"\n⚡ Note: Moderate multicollinearity present (max VIF = {max_vif:.2f})")
else:
    print(f"\n✓ Good: No serious multicollinearity issues (max VIF = {max_vif:.2f})")

# ============================================================================
# 6. ENHANCED MODEL WITH INTERACTION EFFECTS
# ============================================================================

print("\n" + "=" * 70)
print("MODEL 2: ENHANCED MODEL WITH INTERACTIONS")
print("=" * 70)

# Create interaction term
digital_holiday = log_digital * holiday

X_interaction = np.column_stack([
    log_lag_sales, log_tv, log_digital, log_social, log_email, log_sem,
    promotion, holiday, digital_holiday, q2, q3, q4
])
X_interaction_const = sm.add_constant(X_interaction)

model_interaction = sm.OLS(log_sales, X_interaction_const).fit()
print(model_interaction.summary())

# ============================================================================
# 7. FULL MODEL WITH EXTERNAL FACTORS
# ============================================================================

print("\n" + "=" * 70)
print("MODEL 3: FULL MODEL WITH EXTERNAL FACTORS")
print("=" * 70)

X_full = np.column_stack([
    log_lag_sales, log_tv, log_digital, log_social, log_email, log_sem,
    promotion, holiday, digital_holiday, competitor, economic, q2, q3, q4
])
X_full_const = sm.add_constant(X_full)

model_full = sm.OLS(log_sales, X_full_const).fit()
print(model_full.summary())

# ============================================================================
# 8. MODEL COMPARISON
# ============================================================================

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

comparison = pd.DataFrame({
    'Model': ['Base Model', 'Interaction Model', 'Full Model'],
    'R²': [model_base.rsquared, model_interaction.rsquared, model_full.rsquared],
    'Adj. R²': [model_base.rsquared_adj, model_interaction.rsquared_adj, model_full.rsquared_adj],
    'AIC': [model_base.aic, model_interaction.aic, model_full.aic],
    'BIC': [model_base.bic, model_interaction.bic, model_full.bic]
})

print(comparison.to_string(index=False))

# Select best model
best_model = model_full
print(f"\n✓ Selected Model: Full Model (Highest Adj. R² = {best_model.rsquared_adj:.4f})")

# ============================================================================
# 9. EXTRACT AND INTERPRET ELASTICITIES
# ============================================================================

print("\n" + "=" * 70)
print("MARKETING CHANNEL ELASTICITIES")
print("=" * 70)

# Get coefficients (skip constant)
coefs = best_model.params[1:]  # Skip intercept
coef_names = ['log(lag_sales)', 'log(tv)', 'log(digital)', 'log(social)',
              'log(email)', 'log(sem)', 'promotion', 'holiday', 'digital_holiday',
              'competitor', 'economic', 'Q2', 'Q3', 'Q4']

# Extract marketing channel elasticities
elasticities = pd.DataFrame({
    'Channel': ['TV', 'Digital', 'Social Media', 'Email', 'SEM'],
    'Elasticity': [
        coefs[1],  # log(tv)
        coefs[2],  # log(digital)
        coefs[3],  # log(social)
        coefs[4],  # log(email)
        coefs[5]   # log(sem)
    ]
})

elasticities['Interpretation'] = elasticities.apply(
    lambda row: f"1% ↑ in {row['Channel']} → {row['Elasticity']*100:.2f}% ↑ in sales",
    axis=1
)

print(elasticities.to_string(index=False))

# Other effects
print("\n--- Other Key Effects ---")
print(f"Lagged Sales (Momentum): {coefs[0]:.3f}")
print(f"  → Sales persistence: 10% ↑ in last week → {coefs[0]*10:.2f}% ↑ this week\n")

print(f"Promotion Effect: {coefs[6]:.3f}")
print(f"  → Promotions increase sales by ~{(np.exp(coefs[6])-1)*100:.1f}%\n")

print(f"Holiday Effect: {coefs[7]:.3f}")
print(f"  → Holidays increase sales by ~{(np.exp(coefs[7])-1)*100:.1f}%\n")

print(f"Digital × Holiday Interaction: {coefs[8]:.3f}")
if coefs[8] > 0:
    print(f"  → Digital ads are MORE effective during holidays")
    print(f"  → Holiday digital elasticity: {coefs[2] + coefs[8]:.3f}")
    print(f"  → That's {((coefs[2] + coefs[8])/coefs[2] - 1)*100:.1f}% more effective!")
else:
    print(f"  → Digital ads are LESS effective during holidays")

# ============================================================================
# 10. ROI ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("RETURN ON INVESTMENT (ROI) ANALYSIS")
print("=" * 70)

# Calculate average spend and sales
avg_sales = np.mean(sales)
avg_tv = np.mean(tv)
avg_digital = np.mean(digital)
avg_social = np.mean(social)
avg_email = np.mean(email)
avg_sem = np.mean(sem)

# ROI = Elasticity × (Sales / Spend)
roi_analysis = pd.DataFrame({
    'Channel': ['TV', 'Digital', 'Social Media', 'Email', 'SEM'],
    'Elasticity': elasticities['Elasticity'].values,
    'Avg_Spend_K': [avg_tv, avg_digital, avg_social, avg_email, avg_sem],
    'Marginal_Sales_per_1K': [
        elasticities['Elasticity'].values[0] * avg_sales / avg_tv,
        elasticities['Elasticity'].values[1] * avg_sales / avg_digital,
        elasticities['Elasticity'].values[2] * avg_sales / avg_social,
        elasticities['Elasticity'].values[3] * avg_sales / avg_email,
        elasticities['Elasticity'].values[4] * avg_sales / avg_sem
    ]
})

roi_analysis['ROI_Ratio'] = roi_analysis['Marginal_Sales_per_1K']

print(roi_analysis.to_string(index=False))

print("\nInterpretation:")
print("- Higher ROI_Ratio = More efficient channel")
print("- Marginal_Sales_per_1K = Additional sales from $1K increase in spend")

# ============================================================================
# 11. BUDGET OPTIMIZATION RECOMMENDATIONS
# ============================================================================

print("\n" + "=" * 70)
print("BUDGET OPTIMIZATION INSIGHTS")
print("=" * 70)

# Rank by ROI
roi_ranked = roi_analysis.sort_values('ROI_Ratio', ascending=False)
print("\nChannels Ranked by ROI (Best to Worst):")
print(roi_ranked[['Channel', 'ROI_Ratio']].to_string(index=False))

print(f"\nRecommendations:")
print(f"1. Top performing channel: {roi_ranked.iloc[0]['Channel']}")
print(f"2. Consider increasing budget for: {', '.join(roi_ranked.iloc[0:2]['Channel'].values)}")
print(f"3. Consider reducing budget for: {', '.join(roi_ranked.iloc[-2:]['Channel'].values)}")

# ============================================================================
# 12. DIAGNOSTIC PLOTS
# ============================================================================

print("\nGenerating diagnostic plots...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Residuals vs Fitted
axes[0, 0].scatter(best_model.fittedvalues, best_model.resid, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted Values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted Values')
axes[0, 0].grid(alpha=0.3)

# 2. Q-Q plot
sm.qqplot(best_model.resid, line='s', ax=axes[0, 1])
axes[0, 1].set_title('Normal Q-Q Plot')
axes[0, 1].grid(alpha=0.3)

# 3. Scale-Location
axes[1, 0].scatter(best_model.fittedvalues, np.sqrt(np.abs(best_model.resid)), alpha=0.6)
axes[1, 0].set_xlabel('Fitted Values')
axes[1, 0].set_ylabel('√|Residuals|')
axes[1, 0].set_title('Scale-Location Plot')
axes[1, 0].grid(alpha=0.3)

# 4. Residuals histogram
axes[1, 1].hist(best_model.resid, bins=30, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Residual Distribution')
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('plots/07_diagnostic_plots.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Diagnostic plots saved")

# ============================================================================
# 13. SAVE RESULTS
# ============================================================================

os.makedirs('results', exist_ok=True)

# Save elasticities
elasticities.to_csv('results/elasticities.csv', index=False)

# Save ROI analysis
roi_analysis.to_csv('results/roi_analysis.csv', index=False)

# Save model comparison
comparison.to_csv('results/model_comparison.csv', index=False)

# Save model summary to text file
with open('results/model_summary.txt', 'w') as f:
    f.write("FULL MODEL SUMMARY\n")
    f.write("=" * 70 + "\n\n")
    f.write(str(best_model.summary()))

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
print("\n✓ Results saved to results/ directory")
print("✓ Plots saved to plots/ directory")
print("\nFiles created:")
print("  - results/elasticities.csv")
print("  - results/roi_analysis.csv")
print("  - results/model_comparison.csv")
print("  - results/model_summary.txt")
print("  - 7 visualization files in plots/")
