# Conjoint Analysis Methodology

## Table of Contents
1. [What is Conjoint Analysis?](#what-is-conjoint-analysis)
2. [How It Works](#how-it-works)
3. [Statistical Framework](#statistical-framework)
4. [Step-by-Step Process](#step-by-step-process)
5. [Business Applications](#business-applications)
6. [Benefits & Limitations](#benefits--limitations)

---

## What is Conjoint Analysis?

**Conjoint analysis** is a statistical technique used to understand how consumers value different attributes or features of a product or service. It reveals the trade-offs customers make when choosing between options and quantifies the relative importance of each feature.

### Core Principle

Consumers evaluate products as **bundles of attributes** rather than isolated features. Conjoint analysis decomposes overall preferences into the value (utility) of each individual attribute.

**Example**: A TV is not just "a TV"—it's a combination of:
- Screen size (65", 75", 85")
- Resolution (Standard, 4K)
- Brand (Sony, Sharp)
- Price ($2,000, $2,500)

Conjoint analysis reveals:
- How much value each feature adds
- Which features matter most
- How customers trade off features against price
- Optimal product configurations

---

## How It Works

### 1. Survey Design

Present respondents with different **product profiles** (combinations of features) and ask them to rate or rank their preferences.

**Example Product Profiles**:

| Profile | Screen | Resolution | Brand | Price |
|---------|--------|-----------|-------|-------|
| A | 65" | 4K | Sony | $2,000 |
| B | 75" | Standard | Sharp | $2,000 |
| C | 85" | 4K | Sony | $2,500 |
| D | 75" | 4K | Sharp | $2,500 |

Respondent rates each profile on a scale (e.g., 1-10) or ranks them in order of preference.

### 2. Data Collection

Collect preference ratings across multiple product combinations, ensuring:
- **Orthogonal design**: Features vary independently
- **Balanced profiles**: All feature levels appear equally often
- **Sufficient variation**: Enough combinations to estimate all effects

### 3. Statistical Analysis

Use **regression modeling** to estimate part-worth utilities:

```
Preference = β₀ + β₁(Feature1) + β₂(Feature2) + ... + βₙ(Featureₙ) + ε
```

The coefficients (β) represent the **part-worth utilities**—the value each feature adds to overall preference.

### 4. Market Simulation

Use **multinomial logit model** to predict market share:

```
Market Share_product = exp(Utility_product) / Σ exp(Utility_all products)
```

This captures realistic competitive dynamics where higher utility products capture proportionally more market share.

---

## Statistical Framework

### Part-Worth Utility Model

**Assumption**: Total utility is the sum of individual feature utilities:

```
U_total = β₀ + Σ βᵢ × Xᵢ
```

Where:
- `U_total` = Overall product utility
- `β₀` = Intercept (baseline utility)
- `βᵢ` = Part-worth for feature i
- `Xᵢ` = Binary indicator (1 if feature i is present, 0 otherwise)

**Example**:
```
U(Sony 4K 75" at $2,000) = 10.83 + 3.83(4K) + 2.17(Sony) + 0(75") + 0(LowPrice)
                         = 16.83
```

### Attribute Importance

Measures the relative influence of each feature category:

```
Importance_feature = Range_feature / Σ Range_all features
```

Where:
```
Range = Max(part-worth) - Min(part-worth)
```

**Example (Screen Size)**:
```
Range_screen = Max(0, -2.25, 0) - Min(0, -2.25, 0) = 0 - (-2.25) = 2.25

Importance_screen = 2.25 / (2.25 + 3.83 + 2.17 + 1.17) = 2.25 / 9.42 = 23.8%
```

### Willingness to Pay (WTP)

Converts utility into dollar values using price coefficient:

```
WTP_feature = (β_feature / |β_price|) × Price_difference
```

**Example (4K Resolution)**:
```
WTP_4K = (3.83 / |-1.17|) × $500 = 3.27 × $500 = $1,637
```

### Market Share (Multinomial Logit)

Predicts probability of choosing each product:

```
P(choose product j) = exp(Uⱼ) / Σ exp(Uₖ)
```

**Example**:
```
U_own = 16.83  →  exp(16.83) = 20,236,185
U_CompA = 15.66  →  exp(15.66) = 6,329,116
U_CompB = 14.66  →  exp(14.66) = 2,333,730

Share_own = 20,236,185 / (20,236,185 + 6,329,116 + 2,333,730) = 70%
```

---

## Step-by-Step Process

### Phase 1: Research Design

**1. Define Attributes & Levels**
- Identify key product features (e.g., screen size, resolution)
- Determine levels for each attribute (e.g., 65", 75", 85")
- Ensure realistic combinations

**2. Create Product Profiles**
- Use experimental design (orthogonal array, fractional factorial)
- Balance attribute levels across profiles
- Minimize respondent burden (typically 8-20 profiles)

**3. Design Survey**
- Rating scale (1-10) or ranking method
- Clear instructions and visual aids
- Randomize profile order

### Phase 2: Data Collection

**1. Recruit Respondents**
- Target representative sample
- Screen for product category users
- Ensure sufficient sample size (n ≥ 100 recommended)

**2. Administer Survey**
- Online, in-person, or phone
- Monitor response quality
- Check for speeders or straight-liners

**3. Clean Data**
- Remove invalid responses
- Check for missing data
- Verify response patterns

### Phase 3: Statistical Analysis

**1. Estimate Part-Worths**
```r
model <- lm(Preference ~ Feature1 + Feature2 + ... + FeatureN, data = survey_data)
part_worths <- coef(model)
```

**2. Calculate Attribute Importance**
```r
ranges <- apply(part_worth_matrix, 2, function(x) max(x) - min(x))
importance <- ranges / sum(ranges)
```

**3. Compute Willingness to Pay**
```r
wtp <- (part_worths / abs(part_worth_price)) * price_difference
```

**4. Simulate Market Share**
```r
utilities <- calculate_utilities(product_configs)
shares <- exp(utilities) / sum(exp(utilities))
```

### Phase 4: Optimization

**1. Test Product Configurations**
- Vary feature combinations
- Calculate utility for each config
- Predict market share

**2. Optimize Pricing**
- Test range of price points
- Calculate profit at each price
- Account for costs and margins

**3. Identify Optimal Strategy**
- Maximize profit = (Price - Cost) × MarketShare × MarketSize
- Consider competitive responses
- Validate against business constraints

### Phase 5: Reporting

**1. Visualize Results**
- Part-worth charts
- Attribute importance bars
- Market share vs. price curves
- Profit optimization graphs

**2. Strategic Recommendations**
- Optimal product configuration
- Pricing strategy
- Market positioning
- Competitive advantages

---

## Business Applications

### 1. Product Development

**Use**: Design new products with features customers actually value

**Example**: Instead of adding every possible feature, focus investment on high-importance attributes (e.g., 4K resolution over screen size).

**Value**: Avoid over-engineering and reduce development costs.

### 2. Pricing Strategy

**Use**: Set prices based on customer-perceived value rather than just costs

**Example**: Charge premium for features with high WTP (e.g., $1,637 for 4K), discount features with low/negative value (e.g., 85" screen).

**Value**: Optimize revenue and margins.

### 3. Market Segmentation

**Use**: Identify different customer segments with different preferences

**Example**: 
- Segment A: Price-sensitive, values screen size
- Segment B: Quality-focused, values resolution
- Segment C: Brand-loyal, willing to pay for Sony

**Value**: Tailor offerings to each segment.

### 4. Competitive Analysis

**Use**: Understand how your product stacks up against competitors

**Example**: Predict market share against Competitor A (high price) and Competitor B (different brand).

**Value**: Inform competitive positioning and response strategies.

### 5. Portfolio Optimization

**Use**: Decide which product variants to offer in a product line

**Example**: Offer 65" and 75" models, skip 85" (negative preference).

**Value**: Streamline SKUs and reduce complexity.

### 6. Feature Prioritization

**Use**: Determine which features to include in different product tiers

**Example**:
- Basic: 65" Standard Sharp ($1,500)
- Standard: 75" 4K Sharp ($2,000)
- Premium: 75" 4K Sony ($2,400)

**Value**: Clear differentiation and value laddering.

---

## Benefits & Limitations

### Benefits

✅ **Customer-Centric Decisions**
- Base product and pricing decisions on real customer preferences
- Move beyond assumptions to data-driven insights

✅ **Trade-off Analysis**
- Understand what customers are willing to sacrifice
- Quantify feature substitutability (e.g., lower price for fewer features)

✅ **Reduced Risk**
- Test product concepts before expensive development and launch
- Validate ideas with target customers

✅ **Quantitative Insights**
- Precise numerical valuations, not just qualitative feedback
- Statistical significance testing

✅ **Strategic Advantage**
- Identify market gaps and opportunities competitors may have missed
- Optimize feature mix for profitability

✅ **ROI Optimization**
- Invest in features that drive the most customer value
- Avoid spending on low-value attributes

### Limitations

❌ **Survey Fatigue**
- Respondents may tire evaluating many profiles
- Quality degrades with too many combinations
- **Mitigation**: Limit to 8-20 profiles, use adaptive designs

❌ **Hypothetical Bias**
- Stated preferences may differ from actual behavior
- Survey context differs from real purchase situations
- **Mitigation**: Validate with market data, use incentive-compatible designs

❌ **Limited Attributes**
- Can only test a handful of features (typically 4-6)
- May miss important unlisted attributes
- **Mitigation**: Use qualitative research to identify key attributes first

❌ **Additive Assumption**
- Assumes features combine additively (no interactions)
- May miss synergies or conflicts between features
- **Mitigation**: Test interactions if theoretically important

❌ **Static Analysis**
- Preferences may change over time
- Market conditions evolve
- **Mitigation**: Refresh analysis periodically, monitor trends

❌ **Sample Representativeness**
- Results only as good as sample quality
- May not generalize to entire market
- **Mitigation**: Use probability sampling, weight responses

---

## Conclusion

Conjoint analysis is a powerful technique for:
1. Understanding customer preferences
2. Optimizing product configurations
3. Setting data-driven prices
4. Simulating competitive scenarios
5. Maximizing profitability

When properly executed, it provides actionable insights that directly inform product strategy, pricing decisions, and market positioning—transforming customer preferences into business value.

---

**For more information**:
- Green, P. E., & Srinivasan, V. (1990). Conjoint analysis in marketing research: New developments and directions. *Journal of Marketing*, 54(4), 3-19.
- Orme, B. K. (2010). *Getting started with conjoint analysis: Strategies for product design and pricing research*. Research Publishers LLC.
- Louviere, J. J., Hensher, D. A., & Swait, J. D. (2000). *Stated choice methods: Analysis and applications*. Cambridge University Press.
