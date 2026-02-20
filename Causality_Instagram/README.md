# Causal Inference: Instagram Engagement Drivers

**Author:** Shruthi Khurana  
**Program:** MS Business Analytics, UC Davis  
**Tools:** R, Two-Stage Least Squares (2SLS), Instrumental Variables  
**Techniques:** Causal inference, Endogeneity correction, IV regression

---

## 📊 Project Overview

This project uses **advanced causal inference techniques** to identify the true effects of content format choices on Instagram engagement. Unlike correlation analysis, this approach isolates causal effects using Two-Stage Least Squares (2SLS) regression with instrumental variables to address endogeneity.

**Key Challenge:** Simply comparing engagement across post types gives biased results because the same personality traits that make someone choose videos or feature themselves also make their posts more engaging. We need to separate format effects from personality effects.

**Solution:** Instrumental variables that predict format choice but don't directly affect engagement.

---

## 🎯 Business Problem

Instagram content creators face strategic decisions:
- **Should I post videos or photos?**
- **Should I feature myself in complaint posts?**
- **Which format drives more engagement (likes and comments)?**

Standard regression can't answer these questions because:
- Charismatic people post more videos AND get more engagement
- Confident people feature themselves AND get more engagement
- We can't tell if format causes engagement or personality causes both

**Investment at Stake:** Content strategy for 1,000 complaint posts reaching millions of users

---

## 📈 Key Findings

### Causal Effects on Engagement

**Featuring Yourself:**
- **+33.5 likes** (p < 0.001) - Highly significant positive effect
- **+5.7 comments** (p < 0.001) - Drives discussion
- **Interpretation:** Authenticity and emotional connection drive broad engagement

**Posting Video (vs Photo):**
- **-7.3 likes** (p = 0.005) - Reduces virality
- **+8.6 comments** (p < 0.001) - Increases discussion
- **Interpretation:** Videos sacrifice likes for deeper engagement

**Key Trade-Off:**
- Photos: High virality (more likes), low depth
- Videos: Low virality (fewer likes), high depth (more comments)
- **Strategic choice depends on goal:** Awareness vs action

### Control Variables

**Follower Count:** (Strongest predictor)
- **+0.104 likes per follower** (p < 0.001)
- **+0.033 comments per follower** (p < 0.001)
- Each 1,000 followers → +104 likes, +33 comments

**Caption Length:**
- **+0.033 likes per character** (p = 0.139) - Not significant for likes
- **+0.041 comments per character** (p = 0.004) - Significant for comments
- Longer captions drive discussion, not virality

---

## 🔬 Methodology: Why Instrumental Variables?

### The Endogeneity Problem

**Naive Approach (OLS Regression):**
```
Likes = β₀ + β₁(Video) + β₂(FeatureSelf) + ε
```

**Problem:** Video and FeatureSelf correlate with ε (error term)
- Unobserved traits: charisma, confidence, storytelling ability
- These traits affect BOTH format choice AND engagement
- OLS gives biased estimates

**Example:**
- Charismatic people post more videos
- Charismatic people also get more likes
- Is it the video OR the charisma causing likes?
- Can't tell with OLS!

### Two-Stage Least Squares (2SLS) Solution

**Stage 1:** Predict format choice using instruments
```
Video = γ₀ + γ₁(Photography) + γ₂(Followers) + γ₃(Caption Length) + u
FeatureSelf = δ₀ + δ₁(SelfPct) + δ₂(Followers) + δ₃(Caption Length) + v
```

**Stage 2:** Use predicted values in engagement regression
```
Likes = β₀ + β₁(Video_predicted) + β₂(FeatureSelf_predicted) + β₃(Controls) + ε
```

**Result:** Isolates causal effect of format, removes personality bias

---

## 🔑 Instrumental Variables

### Why These Instruments Work

**1. Photography Habit (Instrument for Video)**
- **Definition:** Proportion of user's past posts with camera emoji or photography hashtags
- **Relevance:** People with photography interest more likely to shoot videos (F = 155, p < 2e-16)
- **Exclusion:** Past photography habit doesn't directly affect current post's engagement
- **Logic:** Habit formed long before this specific complaint post

**2. Self-Posting Habit (Instrument for Featuring Self)**
- **Definition:** Proportion of user's past posts featuring themselves
- **Relevance:** People who regularly post selfies likely to feature self again (F = 358, p < 2e-16)
- **Exclusion:** Past selfie frequency doesn't directly affect this post's engagement
- **Logic:** Pre-existing behavior pattern, not related to current post quality

### Statistical Validation

**Instrument Strength (First-Stage F-statistics):**
- Video instrument: **F = 155** (p < 2e-16) ✅ Very strong
- FeatureSelf instrument: **F = 358** (p < 2e-16) ✅ Extremely strong

**Rule of Thumb:** F > 10 indicates strong instrument
- Our instruments: 15-35x stronger than minimum threshold
- No weak instrument problem

**Endogeneity Test (Wu-Hausman):**
- Likes model: **p < 1e-6** ✅ Endogeneity confirmed
- Comments model: **p < 2.6e-11** ✅ Endogeneity confirmed
- **Conclusion:** IV regression necessary; OLS would be biased

**Over-identification Test (Sargan):**
- Not applicable (exactly identified: 2 instruments for 2 endogenous variables)
- Perfect identification - no excess instruments to test

---

## 📊 Detailed Results

### Model 1: Likes

**Regression Output:**
```
Call:
ivreg(IGLikes ~ LengthChar + Followers + Video + FeatureSelf | 
      LengthChar + Followers + Photography + SelfPct)

Coefficients:
                Estimate   Std. Error   t value   Pr(>|t|)    
(Intercept)      12.58      2.86        4.40      1.2e-05 ***
LengthChar        0.03      0.02        1.48      0.139       
Followers         0.10      0.003      35.00      < 2e-16 ***
Video            -7.26      2.59       -2.81      0.005   ** 
FeatureSelf      33.45      1.91       17.55      < 2e-16 ***

R² = 0.6629, Adjusted R² = 0.6615
```

**Interpretation:**
- **Videos reduce likes by 7.3** (all else equal)
- **Featuring yourself adds 33.5 likes** (all else equal)
- **Model explains 66% of variation** in likes
- **Follower count dominates:** 100 followers → +10.4 likes

### Model 2: Comments

**Regression Output:**
```
Call:
ivreg(IGComments ~ LengthChar + Followers + Video + FeatureSelf | 
      LengthChar + Followers + Photography + SelfPct)

Coefficients:
                Estimate   Std. Error   t value   Pr(>|t|)    
(Intercept)       1.60      1.81        0.88      0.378       
LengthChar        0.04      0.01        2.90      0.004   **  
Followers         0.03      0.002      17.79      < 2e-16 ***
Video             8.62      1.64        5.27      1.7e-07 ***
FeatureSelf       5.74      1.21        4.76      2.2e-06 ***

R² = 0.4334, Adjusted R² = 0.4311
```

**Interpretation:**
- **Videos increase comments by 8.6** (all else equal)
- **Featuring yourself adds 5.7 comments** (all else equal)
- **Caption length matters for comments** (+0.04 per character)
- **Model explains 43% of variation** (lower than likes - comments more unpredictable)

---

## 💡 Strategic Implications

### Content Strategy by Goal

**Goal: Maximize Reach/Awareness**
- ✅ Use photos (more likes)
- ✅ Feature yourself (+33.5 likes)
- ✅ Keep captions short
- 📊 Expected: High likes, moderate comments

**Goal: Drive Action/Discussion**
- ✅ Use videos (+8.6 comments)
- ✅ Feature yourself (+5.7 comments)
- ✅ Write longer captions (+0.04 comments/char)
- 📊 Expected: Moderate likes, high comments

**Goal: Corporate Response to Complaints**
- ✅ **Use video format** (more comments = more public pressure)
- ✅ **Feature yourself** (authenticity drives urgency)
- 🎯 Trade-off: Fewer likes but deeper engagement
- **Why:** Brands respond to sustained discussion, not just viral likes

### Instagram Platform Recommendations

**For Users:**
- Encourage victim-centered video complaints
- Surface high-comment posts to brands faster
- Deprioritize like-focused metrics for issue posts

**For Brands:**
- Monitor comment volume, not just likes
- Video complaints signal deeper frustration
- Self-featuring posts indicate authentic grievances

---

## 🔧 Technical Implementation

### Data Structure

```r
# Dataset: IGdata
# N = 1,000 Instagram complaint posts
# Variables:
#   - IGLikes: Number of likes (outcome)
#   - IGComments: Number of comments (outcome)
#   - Video: Binary (1 = video, 0 = photo)
#   - FeatureSelf: Binary (1 = self in post, 0 = not)
#   - LengthChar: Caption length in characters
#   - Followers: Follower count
#   - Photography: % of past posts with camera emoji/photography hashtags (instrument)
#   - SelfPct: % of past posts featuring user (instrument)
```

### R Code Implementation

**Load Packages:**
```r
library(ivreg)  # For IV regression
library(AER)    # For diagnostic tests
library(dplyr)  # For data manipulation
```

**Model 1: Likes**
```r
iv_likes <- ivreg(
  IGLikes ~ LengthChar + Followers + Video + FeatureSelf |  # Second stage
            LengthChar + Followers + Photography + SelfPct,  # First stage
  data = IGdata
)

summary(iv_likes, diagnostics = TRUE)
```

**Model 2: Comments**
```r
iv_comments <- ivreg(
  IGComments ~ LengthChar + Followers + Video + FeatureSelf |
               LengthChar + Followers + Photography + SelfPct,
  data = IGdata
)

summary(iv_comments, diagnostics = TRUE)
```

**Diagnostic Tests:**
```r
# Weak instruments test (automatic with summary)
# Wu-Hausman endogeneity test (automatic with summary)
# Sargan over-identification test (if applicable)
```

---

## 📁 Project Structure

```
Causal-Inference-Instagram-IV/
├── README.md                    # This file
├── analysis.R                   # Complete 2SLS analysis
├── Causality.pdf               # Original homework with full analysis
├── data/
│   └── 06_Social_IV.Rdata      # Dataset (if sharable)
└── results/
    ├── iv_likes_results.csv    # Likes model coefficients
    └── iv_comments_results.csv # Comments model coefficients
```

---

## 🎓 Skills Demonstrated

### Statistical Expertise
- **Causal inference:** Distinguishing correlation from causation
- **Instrumental variables:** Identifying and validating instruments
- **Two-stage least squares (2SLS):** Advanced regression technique
- **Endogeneity correction:** Addressing omitted variable bias
- **Diagnostic testing:** Weak instruments, endogeneity, over-identification

### Econometric Rigor
- **First-stage F-statistics:** Instrument relevance (F > 100)
- **Wu-Hausman test:** Endogeneity validation (p < 1e-6)
- **Exclusion restriction:** Theoretical and empirical validation
- **Exactly identified models:** 2 instruments for 2 endogenous variables

### Business Application
- **Content strategy:** Video vs photo, self-feature vs not
- **Goal-oriented recommendations:** Awareness vs action
- **Platform insights:** Instagram algorithm implications
- **Stakeholder communication:** Brands and users

---

## 💼 Real-World Applications

### Where This Methodology Applies

**Social Media Marketing:**
- Does influencer endorsement cause sales or just correlation?
- Do hashtags drive reach or do viral posts use more hashtags?
- Does posting frequency cause engagement or vice versa?

**Product Development:**
- Does feature usage cause retention or do engaged users use more features?
- Do notifications drive engagement or do engaged users enable notifications?

**Business Analytics:**
- Does customer service quality cause loyalty or do loyal customers rate higher?
- Do promotions drive sales or do we run promotions when sales are low?

**Key Insight:** Whenever X and Y correlate but causality is unclear due to unobserved factors, IV regression can isolate true causal effects.

---

## 🚀 Extensions & Future Work

### Potential Enhancements

**1. Heterogeneous Treatment Effects**
- Does video effect differ by follower count?
- Do micro-influencers benefit more from self-featuring?
- Segment analysis by user type

**2. Additional Outcomes**
- Shares/saves as depth metrics
- Time to corporate response
- Issue resolution rate

**3. Alternative Instruments**
- Past video view duration (for video preference)
- Past profile photo changes (for self-confidence)
- Account age (for platform comfort)

**4. Robustness Checks**
- Propensity score matching (alternative causal method)
- Regression discontinuity (if threshold exists)
- Difference-in-differences (if time variation available)

---

## 📚 Theoretical Foundation

### Why IV Regression?

**The Fundamental Problem of Causal Inference:**
- We observe: Correlation between X (format) and Y (engagement)
- We want: Causal effect of X on Y
- Challenge: Unobserved confounders (personality, skill)

**IV Regression Requirements:**
1. **Relevance:** Instrument correlates with endogenous variable
   - ✅ Photography predicts Video (F = 155)
   - ✅ SelfPct predicts FeatureSelf (F = 358)

2. **Exclusion:** Instrument only affects outcome through treatment
   - ✅ Past photography habit doesn't directly affect current post likes
   - ✅ Past selfie rate doesn't directly affect current post likes

3. **Independence:** Instrument uncorrelated with error term
   - ✅ Past habits formed before current complaint
   - ✅ Not related to current post quality/grievance

### Comparison to Other Methods

| Method | Strength | Weakness | When to Use |
|--------|----------|----------|-------------|
| **OLS** | Simple, efficient | Biased if endogenous | No unobserved confounders |
| **IV/2SLS** | Unbiased causal estimates | Requires valid instruments | Endogeneity present |
| **RCT** | Gold standard | Expensive, sometimes unethical | Full experimental control |
| **Matching** | Intuitive | Only controls for observables | Many control variables |
| **RDD** | Credible quasi-experiment | Needs discontinuity | Sharp cutoff exists |

**Our Case:** IV/2SLS appropriate because:
- Can't randomize post format (ethical/practical concerns)
- Unobserved confounders (personality) create bias
- Valid instruments available (past habits)

---

## 📊 Model Diagnostics Summary

**Likes Model:**
- R² = 0.6629 (explains 66% of variation)
- Weak instruments test: F = 155, 358 (both p < 2e-16) ✅
- Wu-Hausman test: p < 1e-6 (endogeneity confirmed) ✅
- All key variables significant at p < 0.01

**Comments Model:**
- R² = 0.4334 (explains 43% of variation)
- Weak instruments test: F = 155, 358 (both p < 2e-16) ✅
- Wu-Hausman test: p < 2.6e-11 (endogeneity confirmed) ✅
- All key variables significant at p < 0.001

**Conclusion:** Models satisfy all IV requirements and provide credible causal estimates.

---

## 👤 About the Author

**Shruthi Khurana**

**Education:**
- MS Business Analytics, UC Davis - GPA 4.0
- MBA, Xavier School of Management, India

**Experience:**
- Marketing Data Analyst, Lagunitas Brewing Company
- 5+ years in banking and analytics

**Skills:** R, Python, Causal Inference, Econometrics, Statistical Modeling

---

## 📧 Contact

**GitHub:** [shruthi-khurana](https://github.com/shruthi-khurana)  
**LinkedIn:** [Shruthi Khurana](https://linkedin.com/in/shruthi-khurana)

---

## 📄 License

This project is for educational and portfolio purposes. Methodology applicable to any social media or content strategy analysis.

---

*This project demonstrates advanced causal inference techniques rarely seen in analytics portfolios. Understanding when and how to use instrumental variables is a valuable skill for tackling real-world business questions where correlation doesn't equal causation.*

**Last Updated:** February 2026
