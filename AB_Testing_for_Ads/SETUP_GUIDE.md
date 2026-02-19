# A/B Testing Project - Setup Guide

## 🚀 Quick Start

This project analyzes an Instagram ad A/B test with 100,000 impressions across 4 variants to determine optimal ad creative and stopping point.

### Prerequisites

```r
# Required R packages
install.packages(c("dplyr", "knitr", "kableExtra", "ggplot2"))
```

### Running the Analysis

```r
# Load your data file (IGAds.RData)
load("IGAds.RData")

# Run the complete analysis
source("analysis.R")
```

---

## 📊 What This Analysis Does

### Question 1: Which Ad is Best?

**Tests performed:**
- Overall proportion test (chi-square)
- Pairwise proportion tests with Bonferroni correction
- ANOVA for revenue analysis
- Tukey HSD for pairwise revenue comparisons

**Outputs:**
- Conversion rates by ad
- Statistical significance of differences
- Revenue per conversion
- Recommendation by campaign goal

### Question 2: When Should We Stop Testing?

**Tests performed:**
- Sequential testing across 10 rounds
- P-value evolution analysis
- Multi-armed bandit simulation
- Cost-benefit analysis of delayed action

**Outputs:**
- CTR by round for each ad
- Statistical significance timeline
- Optimal stopping point (Round 2)
- Financial impact of delayed decision ($10K)

---

## 📁 Project Structure

```
AB-Testing-Ad-Optimization/
├── README.md                    # Complete project documentation
├── EXECUTIVE_SUMMARY.md         # Business-focused summary
├── SETUP_GUIDE.md              # This file
├── analysis.R                   # Main R script with all analysis
│
├── data/
│   └── IGAds.RData             # Dataset (not included - proprietary)
│
└── results/
    ├── ctr_by_round.csv        # CTR performance across rounds
    ├── conversion_summary.csv   # Overall conversion metrics
    └── revenue_summary.csv      # Revenue analysis results
```

---

## 🎯 Key Results

**Best Performing Ads:**
- **Ad A:** 5.05% CTR (best for conversions)
- **Ad C:** $3.59 revenue/conversion (best for revenue)
- **Ad B:** Underperformer on both metrics

**Statistical Decision Point:**
- **Round 2:** Statistical significance established (p < 0.0001)
- **Recommendation:** Stop Ad B after Round 2
- **Cost of delay:** $10,025 revenue loss

**Methodology Improvement:**
- Traditional A/B: Equal allocation throughout
- Multi-armed bandit: Adaptive allocation
- **Expected benefit:** 30-40% sample size reduction

---

## 💻 Customizing for Your Data

### Data Format Required

Your dataset should have these columns:
- `Condition`: Ad variant (A, B, C, Control)
- `Conversion`: Binary (1 = converted, 0 = not converted)
- `Revenue`: Numeric (revenue per impression, 0 if no conversion)

### Modifying Parameters

```r
# In analysis.R, you can adjust:

# Number of rounds
n_rounds <- 10  # Change to your preferred number

# Impressions per round
impressions_per_round <- 10000  # Adjust based on your data

# Significance threshold
sig_threshold <- 0.001  # More conservative: 0.0001, more liberal: 0.01

# Multiple testing correction
p.adjust.method <- "bonferroni"  # Or "holm", "BH", "BY"
```

---

## 📈 Adding Visualizations

The analysis script generates data that can be visualized. Here are some examples:

### CTR Comparison Plot

```r
library(ggplot2)

# Read results
ctr_data <- read.csv("results/ctr_by_round.csv")

# Create plot
ggplot(ctr_data, aes(x = Round)) +
  geom_line(aes(y = A, color = "Ad A"), size = 1) +
  geom_line(aes(y = B, color = "Ad B"), size = 1) +
  geom_line(aes(y = C, color = "Ad C"), size = 1) +
  geom_line(aes(y = Control, color = "Control"), size = 1) +
  labs(title = "CTR by Round",
       y = "Click-Through Rate (%)",
       color = "Variant") +
  theme_minimal()
```

### Statistical Significance Evolution

```r
# P-value evolution plot
ggplot(ctr_data, aes(x = Round, y = pvalue_A_vs_B)) +
  geom_line(size = 1, color = "steelblue") +
  geom_hline(yintercept = 0.001, linetype = "dashed", color = "red") +
  geom_point(size = 3) +
  scale_y_log10() +
  labs(title = "Statistical Significance Over Time",
       subtitle = "P-value: Ad A vs Ad B",
       y = "P-value (log scale)",
       caption = "Red line: Significance threshold (p < 0.001)") +
  theme_minimal()
```

### Revenue Boxplot

```r
# Revenue distribution by ad
conversions <- subset(IGAds, Conversion == 1)

ggplot(conversions, aes(x = Condition, y = Revenue, fill = Condition)) +
  geom_boxplot() +
  labs(title = "Revenue Distribution by Ad Variant",
       y = "Revenue per Conversion ($)") +
  theme_minimal() +
  theme(legend.position = "none")
```

---

## 🔬 Understanding the Statistical Tests

### Proportion Test

**What it does:** Compares conversion rates across groups  
**When to use:** Testing if CTRs are different  
**Output:** Chi-square statistic and p-value

**Interpretation:**
- p < 0.05: At least one group is significantly different
- Small p-value: Strong evidence of differences

### Bonferroni Correction

**What it does:** Adjusts p-values for multiple comparisons  
**Why needed:** Testing 4 groups = 6 pairwise comparisons  
**How it works:** Multiplies each p-value by number of comparisons

**Example:**
- Uncorrected p-value: 0.01
- Bonferroni correction: 0.01 × 6 = 0.06
- Now not significant at α = 0.05 level

### ANOVA

**What it does:** Compares means across groups  
**When to use:** Testing if average revenues differ  
**Output:** F-statistic and p-value

**Follow-up:** If significant, use Tukey HSD to find which pairs differ

### Tukey HSD

**What it does:** Pairwise comparisons with family-wise error control  
**Output:** Confidence intervals for each pair  
**Interpretation:** If CI doesn't include 0, pair is significantly different

---

## 🎓 Extending This Analysis

### 1. Add Confidence Intervals

```r
# For CTR differences
prop.test(x = c(conv_A, conv_B),
          n = c(n_A, n_B),
          conf.level = 0.95)
```

### 2. Calculate Effect Sizes

```r
# Cohen's h for proportions
p1 <- ctr_A / 100
p2 <- ctr_B / 100
cohens_h <- 2 * (asin(sqrt(p1)) - asin(sqrt(p2)))
```

### 3. Power Analysis

```r
library(pwr)

# Required sample size
pwr.2p.test(h = 0.2,           # Small effect size
            sig.level = 0.001,  # Significance level
            power = 0.8)        # Desired power
```

### 4. Bayesian A/B Testing

```r
library(bayesAB)

# Bayesian approach
bayesian_test <- bayesTest(conversions_A, 
                           conversions_B,
                           priors = c('alpha' = 1, 'beta' = 1))
```

---

## 💡 Interview Talking Points

### 30-Second Pitch
"I analyzed an Instagram A/B test with 100K impressions and found Ad A had the highest CTR at 5.05%. Using sequential testing, I discovered statistical significance emerged by Round 2, but the test continued for 8 more rounds, costing $10K in lost revenue. I recommended implementing multi-armed bandit methodology to automatically stop underperformers early, reducing sample sizes by 30-40%."

### Technical Deep-Dive
- **Multiple testing:** Why Bonferroni? Controls family-wise error rate
- **Sequential testing:** How to balance Type I and II errors
- **Multi-armed bandit:** Exploration vs exploitation trade-off
- **Power analysis:** How to determine sample size requirements

### Business Impact
- **Immediate:** Use Ad A for conversions, Ad C for revenue
- **Process:** Implement sequential testing with early stopping
- **Financial:** Save $10K per 100K impressions through optimization
- **Strategic:** Framework applies to all creative testing

---

## 🐛 Troubleshooting

### Data Loading Issues

```r
# If load() doesn't work
load("IGAds.RData")

# Check if data loaded
ls()  # Should see "IGAds"

# Check data structure
str(IGAds)
head(IGAds)
```

### Missing Packages

```r
# Check if package is installed
if (!require("dplyr")) install.packages("dplyr")

# Load package
library(dplyr)
```

### Significance Not Matching

**Possible causes:**
- Different random seed (if data has randomization)
- Different R version
- Different package versions
- Data preprocessing differences

**Solutions:**
- Set seed: `set.seed(123)`
- Check R version: `R.version`
- Update packages: `update.packages()`

---

## 📚 Additional Resources

### Statistical Testing
- [Power Analysis in R](https://www.statmethods.net/stats/power.html)
- [Multiple Testing Correction](https://en.wikipedia.org/wiki/Multiple_comparisons_problem)
- [Bonferroni vs Holm](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6099145/)

### Multi-Armed Bandits
- [Bandit Algorithms Book](https://tor-lattimore.com/downloads/book/book.pdf)
- [A/B Testing vs MAB](https://vwo.com/blog/multi-armed-bandit-algorithm/)
- [Thompson Sampling](https://en.wikipedia.org/wiki/Thompson_sampling)

### Practical A/B Testing
- [Evan Miller's Tools](https://www.evanmiller.org/ab-testing/)
- [Optimizely Stats Engine](https://www.optimizely.com/statistics/)
- [Google Optimize](https://support.google.com/optimize/)

---

## ✅ Checklist Before Finalizing

- [ ] Data file (IGAds.RData) is in data/ folder
- [ ] All required packages installed
- [ ] analysis.R runs without errors
- [ ] Results saved to results/ directory
- [ ] Reviewed all outputs for accuracy
- [ ] Compared with expected results
- [ ] Documented any custom modifications
- [ ] Created visualizations
- [ ] Prepared presentation/summary

---

## 📧 Contact

**Shruthi Khurana**  
MS Business Analytics, UC Davis  
Marketing Data Analyst, Lagunitas Brewing Company

**GitHub:** [shruthi-khurana](https://github.com/shruthi-khurana)  
**LinkedIn:** [Shruthi Khurana](https://linkedin.com/in/shruthi-khurana)

Questions or suggestions? Feel free to reach out!

---

*Last Updated: February 2026*
