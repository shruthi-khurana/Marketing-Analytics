# TV Product Conjoint Analysis

A comprehensive conjoint analysis project examining consumer preferences for television products, analyzing trade-offs between screen size, resolution, brand, and price to optimize product positioning and pricing strategy.

## 📊 Project Overview

This project uses **conjoint analysis** to understand how consumers value different TV attributes and to determine optimal pricing strategies. The analysis reveals customer preferences, willingness to pay for specific features, and identifies the profit-maximizing price point.

### Key Findings

- **Optimal Price**: $2,400
- **Maximum Profit**: $45,583
- **Market Share**: 48%
- **Recommended Product**: Sony 4K 75-inch TV

## 🎯 Business Problem

How should a TV manufacturer position and price their product to maximize profitability while appealing to quality-focused consumers who remain price-sensitive?

## 🔍 Methodology

### Conjoint Analysis Approach

1. **Survey Design**: Presented respondents with different TV profiles combining various features
2. **Preference Ratings**: Collected consumer ratings for each product profile
3. **Regression Modeling**: Estimated part-worth utilities for each feature
4. **Market Simulation**: Used multinomial logit model to predict market share
5. **Optimization**: Identified profit-maximizing price point

### Features Analyzed

| Feature | Levels |
|---------|--------|
| **Screen Size** | 65", 75", 85" |
| **Resolution** | Standard, 4K |
| **Brand** | Sony, Sharp |
| **Price** | Low ($2,000), High ($2,500) |

## 📈 Key Results

### Part-Worth Utilities

| Attribute | Utility | Interpretation |
|-----------|---------|----------------|
| Intercept (Baseline) | 10.83 | Base utility for 65" Sharp non-4K TV |
| 4K Resolution | +3.83 | Strong preference for better display quality |
| Sony Brand | +2.17 | Moderate brand preference |
| 75" Screen | ~0 | Indifferent to mid-size upgrade |
| 85" Screen | -2.25 | Negative preference for largest size |
| High Price | -1.17 | Price sensitivity penalty |

### Attribute Importance

```
Resolution:    40.65%  ████████████████████████████████████████
Brand:         23.00%  ███████████████████████
Screen Size:   23.78%  ███████████████████████
Price:         12.40%  ████████████
```

**Insight**: Resolution is the most valued feature, followed by brand and screen size. Price sensitivity is relatively low, indicating willingness to pay for quality.

### Willingness to Pay (WTP)

- **4K Resolution**: $1,637
- **Sony Brand**: $926
- **75" Screen**: ~$0
- **85" Screen**: ~$0 (negative preference)

### Market Share Analysis

- **Below $2,500**: 70% market share
- **At/Above $2,500**: Drops to 42% (price penalty triggers)
- **Critical threshold**: $2,500 represents psychological pricing barrier

### Profit Optimization

![Profit Curve](docs/profit_curve.png)

- **Optimal Price**: $2,400
- **Maximum Profit**: $45,583
- **Break-even**: $2,000
- **Pricing Strategy**: Stay below $2,500 threshold to maintain high market share

## 💡 Strategic Recommendations

### Product Positioning

**"Premium Quality at Accessible Pricing"**

Target consumers who:
- Prioritize display technology (4K resolution)
- Trust established brands (Sony)
- Value quality over cost savings
- Remain sensitive to ultra-premium pricing tiers

### Optimal Product Configuration

- **Screen Size**: 75 inches
- **Resolution**: 4K
- **Brand**: Sony
- **Price**: $2,400

### Why This Works

1. **Delivers high-importance features** (Resolution: 40.65%, Brand: 23%)
2. **Stays below psychological threshold** ($2,500 triggers steep share loss)
3. **Captures quality-focused segment** (low price sensitivity: 12.4%)
4. **Maximizes profit** while maintaining 70% market share

## 🛠️ Technical Implementation

### Dependencies

```r
# R packages required
library(readxl)  # Data import
library(stats)   # Regression modeling
```

### Running the Analysis

```r
# Load the function
source("conjoint_analysis.R")

# Run analysis
results <- conjoint_analysis(
  preferences_file = "data/Design_Matrix.xlsx",
  own_design = c(
    "Resolution 4K = 1" = 1,
    "Sony = 1" = 1,
    "Price (low = 0; hi =1)" = 0,
    "Screen 75 inch" = 1,
    "Screen 85 inch" = 0
  ),
  compA_design = c(...),  # Competitor A configuration
  compB_design = c(...),  # Competitor B configuration
  feature_costs = c(1000, 500, 1000, 250, 250)
)

# View results
print(results$Partworth_Table)
print(results$Attribute_Importance)
print(results$Optimal_Price)
```

### Function Outputs

The `conjoint_analysis()` function returns:

- **Partworth_Table**: Feature utility estimates with standard errors and t-values
- **Attribute_Importance**: Relative importance of each feature category
- **Willingness_to_Pay**: Dollar value for each feature upgrade
- **Market_Share**: Predicted share for own brand vs. competitors
- **Optimal_Price**: Profit-maximizing price point
- **Maximum_Profit**: Expected profit at optimal price

## 📁 Repository Structure

```
conjoint-analysis-project/
├── README.md                          # This file
├── conjoint_analysis.R                # Main analysis function
├── analysis.Rmd                       # Full R Markdown analysis
├── data/
│   └── Design_Matrix.xlsx            # Survey preference data
├── docs/
│   ├── methodology.md                # Detailed methodology
│   └── findings.md                   # Complete findings report
└── outputs/
    ├── partworth_table.csv           # Part-worth estimates
    ├── attribute_importance.csv      # Feature importance
    ├── market_share_plot.png         # Market share vs. price
    └── profit_plot.png               # Profit vs. price
```

## 📊 Visualizations

### Market Share vs. Price

The market share curve shows a dramatic drop at the $2,500 threshold, validating the $2,400 optimal price point.

### Profit vs. Price

Profit peaks at $2,400, with steep declines on either side due to:
- **Below $2,400**: Lower margins
- **Above $2,500**: Price penalty reduces demand

## 🎓 What is Conjoint Analysis?

Conjoint analysis is a statistical technique that:

- Reveals how customers value different product features
- Quantifies trade-offs consumers make when choosing between options
- Enables data-driven product development and pricing decisions
- Reduces risk by testing concepts before launch

### Business Applications

✅ **Product Development** - Design products with features customers actually value  
✅ **Pricing Strategy** - Set prices based on perceived value, not just costs  
✅ **Market Segmentation** - Identify customer segments with different preferences  
✅ **Competitive Analysis** - Understand positioning vs. competitors  
✅ **Portfolio Optimization** - Decide which product variants to offer  

## 🔬 Methodology Details

### Statistical Model

Part-worth utilities estimated using ordinary least squares (OLS) regression:

```
Utility = β₀ + β₁(Resolution) + β₂(Brand) + β₃(Price) + β₄(Screen75) + β₅(Screen85) + ε
```

Market share predicted using multinomial logit:

```
Market Share = exp(Utility_own) / Σ exp(Utility_all)
```

### Attribute Importance Calculation

```
Importance(feature) = Range(feature) / Σ Range(all features)
```

Where Range = Max(part-worth) - Min(part-worth)

### Willingness to Pay

```
WTP(feature) = (Part-worth_feature / |Part-worth_price|) × Price_difference
```

## 📝 Key Learnings

1. **Resolution dominates**: Display quality is worth $1,637 to consumers
2. **Brand matters**: Sony commands $926 premium
3. **Size indifference**: Consumers don't value screens above 65"
4. **Price threshold**: $2,500 is a psychological barrier
5. **Quality positioning**: Premium features work when priced accessibly

## 🚀 Future Enhancements

- [ ] Add customer segmentation analysis
- [ ] Test additional price points ($2,200-$2,450)
- [ ] Include more brand options
- [ ] Analyze 55" screen size option
- [ ] Add feature: Smart TV capabilities
- [ ] Conduct sensitivity analysis on costs
- [ ] Build interactive Shiny dashboard

## 👥 Contributors

**Shruthi Khurana** - Primary Analysis & Strategic Recommendations

Team Members: Akansha Totre, Niti Chirag Patel, Shivneel Prasad

## 📄 License

This project is available for educational and portfolio purposes.

## 📧 Contact

For questions or collaboration opportunities, please reach out via:
- [LinkedIn](https://www.linkedin.com/in/shruthi-khurana/)
- [Email](skkhurana@ucdavis.edu)

---

*Part of BAx 442 Analytics coursework of MSBA at UC Davis for demonstrating proficiency in conjoint analysis, market research, and data-driven pricing strategy.*
