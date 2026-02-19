# Marketing Mix Modeling - Setup and Run Guide

## Quick Start

### Step 1: Generate Data
```bash
python 01_generate_data.py
```

This creates `marketing_mix_data.csv` with 156 weeks of realistic e-commerce marketing data.

### Step 2: Run Analysis (Python version)
```bash
# Install required packages first
pip install statsmodels scikit-learn seaborn matplotlib pandas numpy

# Run the analysis
python 02_mmm_analysis.py
```

### Step 3: Run Analysis (R version - Alternative)
```bash
Rscript 02_mmm_analysis.R
```

## What Gets Generated

### Data File
- `marketing_mix_data.csv` - 156 weeks of marketing and sales data

### Results Directory
- `elasticities.csv` - Marketing channel elasticities
- `roi_analysis.csv` - ROI calculations for each channel
- `model_comparison.csv` - Performance metrics for all models  
- `model_summary.txt` - Detailed regression output

### Plots Directory
1. `01_sales_trend.png` - Sales over time with holiday markers
2. `02_marketing_spend.png` - Spend by channel over time
3. `03_sales_vs_digital.png` - Relationship between digital spend and sales
4. `04_sales_vs_tv.png` - Relationship between TV spend and sales
5. `05_promotion_effect.png` - Sales distribution with/without promotions
6. `06_holiday_effect.png` - Sales distribution holiday vs non-holiday
7. `07_diagnostic_plots.png` - Model diagnostic plots

## Key Findings You'll Generate

### Elasticities
- **Digital**: 0.12 (most effective channel)
- **Social Media**: 0.10
- **SEM**: 0.09
- **TV**: 0.08
- **Email**: 0.06

### Insights
- Digital ads are ~35% more effective during holidays
- Promotions increase sales by ~16%
- Strong sales momentum (30% carryover from previous week)
- No multicollinearity issues (all VIF < 4)

### Recommendations
- Increase: Digital and Social Media budgets
- Maintain: SEM and TV
- Optimize: Email marketing or reallocate budget

## Customization Ideas

Want to customize for your portfolio? Try:

1. **Different Industry**
   - Change variables in `01_generate_data.py`
   - Example: Beer → add `seasonal_temperature`, `event_sponsorships`

2. **More Channels**
   - Add: Influencer marketing, podcast ads, affiliate marketing
   - Modify data generation to include new variables

3. **Advanced Analysis**
   - Add adstock/decay effects (advertising has lagged impact)
   - Test saturation curves (non-linear diminishing returns)
   - Apply Ridge/Lasso for channel selection

4. **Different Transformations**
   - Try square root instead of log
   - Test polynomial terms
   - Add splines for non-linear effects

## Presenting This Project

### On GitHub README
- Lead with business impact ("Optimized $X million marketing budget")
- Show key visualizations first
- Explain methodology clearly
- Include actionable insights

### In Interviews
- Start with business problem
- Show the data
- Explain model choice (why log-log?)
- Present insights visually
- End with recommendations

### Sample Interview Answer
"I built a Marketing Mix Model to optimize budget allocation for an e-commerce company. Using log-log regression on 3 years of weekly data across 5 marketing channels, I calculated elasticities showing digital ads had the highest ROI at 0.12. I also discovered digital ads were 35% more effective during holidays through interaction terms. This led to recommendations to shift 20% of budget from email to digital during Q4, potentially increasing sales by 8%."

## Troubleshooting

**Issue**: Can't install statsmodels
**Solution**: Use R version instead, or simplify Python version to use basic numpy linear algebra

**Issue**: Plots not saving
**Solution**: Ensure `plots/` and `results/` directories exist:
```python
import os
os.makedirs('plots', exist_ok=True)
os.makedirs('results', exist_ok=True)
```

**Issue**: Want to use your own data
**Solution**: Replace `marketing_mix_data.csv` with your data. Ensure columns include:
- sales (dependent variable)
- marketing channel spend variables
- Control variables (promotions, seasonality, etc.)

## Next Steps

After completing this project:

1. **Add to GitHub**
   - Create repository: `marketing-mix-modeling`
   - Include all code, plots, and comprehensive README
   - Add to your portfolio website

2. **Enhance Your Resume**
   - "Developed Marketing Mix Model using log-log regression to quantify $XM marketing ROI"
   - "Identified digital advertising as highest performing channel (elasticity 0.12)"
   - "Recommended budget reallocation saving $XK annually"

3. **Prepare for Interviews**
   - Practice explaining elasticity concept
   - Be ready to discuss model assumptions
   - Know your limitations (synthetic data, simplified model)
   - Prepare 2-minute and 5-minute versions

4. **Connect to Your Experience**
   - Lagunitas: "Similar to how I analyzed YouTube comment sentiment, MMM quantifies marketing impact"
   - UC Davis: "Applied course concepts (log transformations, VIF) to real marketing problem"
   - Axis Bank: "Like customer analytics, this helps optimize resource allocation"

## Additional Resources

- **Books**: "Marketing Mix Modeling" by Dominique M. Hanssens
- **Online**: Google's Lightweight MMM (open source framework)
- **Industry**: Meta's Robyn MMM tool (open source)
- **Academic**: Papers on marketing response models and attribution

Good luck with your portfolio project!
