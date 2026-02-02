# ==============================================================================
# TV Product Conjoint Analysis
# ==============================================================================
# Author: Shruthi Khurana
# Description: Analyze consumer preferences for TV products to optimize 
#              product positioning and pricing strategy
# ==============================================================================

#' Perform Conjoint Analysis for TV Product Preferences
#'
#' This function analyzes customer preferences for TV products with different
#' features (screen size, resolution, brand, price) to determine optimal
#' product configuration and pricing strategy.
#'
#' @param preferences_file Path to Excel file containing preference ratings
#' @param own_design Named vector specifying your product's feature configuration
#' @param compA_design Named vector specifying Competitor A's configuration
#' @param compB_design Named vector specifying Competitor B's configuration
#' @param feature_costs Numeric vector of costs for each feature level
#'
#' @return List containing:
#'   - Partworth_Table: Feature utility estimates
#'   - Attribute_Importance: Relative importance of each feature
#'   - Willingness_to_Pay: Dollar value for each feature
#'   - Market_Share: Predicted market share vs competitors
#'   - Optimal_Price: Profit-maximizing price point
#'   - Maximum_Profit: Expected profit at optimal price
#'
#' @examples
#' results <- conjoint_analysis(
#'   preferences_file = "data/Design_Matrix.xlsx",
#'   own_design = c("Resolution 4K = 1" = 1, "Sony = 1" = 1, ...),
#'   compA_design = c(...),
#'   compB_design = c(...),
#'   feature_costs = c(1000, 500, 1000, 250, 250)
#' )

conjoint_analysis <- function(
  preferences_file,
  own_design,
  compA_design,
  compB_design,
  feature_costs
) {
  
  # Load required library
  library(readxl)
  
  # ===========================================================================
  # 1. DATA IMPORT
  # ===========================================================================
  
  data <- read_excel(preferences_file)
  
  # ===========================================================================
  # 2. PART-WORTH ESTIMATION
  # ===========================================================================
  # Estimate utility values for each feature using linear regression
  
  model <- lm(
    Preference ~ `Resolution 4K = 1` + 
                 `Sony = 1` + 
                 `Price (low = 0; hi =1)` + 
                 `Screen 75 inch` + 
                 `Screen 85 inch`,
    data = data
  )
  
  # Extract coefficients, standard errors, and t-values
  coef_est <- summary(model)$coefficients
  
  partworth <- coef_est[, "Estimate"]
  se <- coef_est[, "Std. Error"]
  tval <- coef_est[, "Estimate"] / coef_est[, "Std. Error"]
  
  # Clean names by removing backticks for consistent indexing
  names(partworth) <- gsub("`", "", names(partworth))
  names(se) <- gsub("`", "", names(se))
  names(tval) <- gsub("`", "", names(tval))
  
  # Create results table
  partworth_table <- data.frame(
    Partworth = partworth,
    SE = se,
    t_value = tval,
    row.names = names(partworth)
  )
  
  # ===========================================================================
  # 3. ATTRIBUTE IMPORTANCE
  # ===========================================================================
  # Calculate relative importance of each feature category
  
  # Screen size: Range across 65", 75", 85" options
  screen_75_pw <- partworth_table["Screen 75 inch", "Partworth"]
  screen_85_pw <- partworth_table["Screen 85 inch", "Partworth"]
  screen_range <- max(screen_75_pw, screen_85_pw, 0) - 
                  min(screen_75_pw, screen_85_pw, 0)
  
  # Resolution: Range between standard and 4K
  resolution_pw <- partworth_table["Resolution 4K = 1", "Partworth"]
  resolution_range <- abs(resolution_pw)
  
  # Brand: Range between Sony and non-Sony
  brand_pw <- partworth_table["Sony = 1", "Partworth"]
  brand_range <- abs(brand_pw)
  
  # Price: Range between low and high price
  price_pw <- partworth_table["Price (low = 0; hi =1)", "Partworth"]
  price_range <- abs(price_pw)
  
  # Calculate total range for normalization
  sum_range <- screen_range + resolution_range + brand_range + price_range
  
  # Calculate normalized importance percentages
  screen_imp <- screen_range / sum_range
  resolution_imp <- resolution_range / sum_range
  brand_imp <- brand_range / sum_range
  price_imp <- price_range / sum_range
  
  # Create importance table
  imp_table <- data.frame(
    Screen = screen_imp,
    Resolution = resolution_imp,
    Brand = brand_imp,
    Price = price_imp
  )
  
  # ===========================================================================
  # 4. WILLINGNESS TO PAY
  # ===========================================================================
  # Calculate dollar value consumers place on each feature
  
  # Price difference between low and high price tiers
  price_diff <- 500  # $2,500 - $2,000
  
  # Calculate WTP by converting utility to dollars
  # WTP = (feature utility / price utility) * price difference
  wtp_screen_75 <- screen_75_pw * price_diff / abs(price_pw)
  wtp_screen_85 <- screen_85_pw * price_diff / abs(price_pw)
  wtp_4k <- resolution_pw * price_diff / abs(price_pw)
  wtp_sony <- brand_pw * price_diff / abs(price_pw)
  
  # Create WTP table
  wtp_table <- data.frame(
    Screen_75 = wtp_screen_75,
    Screen_85 = wtp_screen_85,
    Resolution_4k = wtp_4k,
    Brand_Sony = wtp_sony
  )
  
  # ===========================================================================
  # 5. MARKET SHARE PREDICTION
  # ===========================================================================
  # Use multinomial logit model to predict market share
  
  # Helper function to calculate total utility for a product design
  utility <- function(design) {
    u <- partworth["(Intercept)"]
    for (feature in names(design)) {
      if (feature %in% names(partworth)) {
        u <- u + partworth[feature] * design[feature]
      }
    }
    return(u)
  }
  
  # Calculate utilities for all products
  u_own <- utility(own_design)
  u_A <- utility(compA_design)
  u_B <- utility(compB_design)
  
  # Apply multinomial logit choice model
  exp_u <- exp(c(u_own, u_A, u_B))
  shares <- exp_u / sum(exp_u)
  
  # Create market share table
  market_share <- data.frame(
    Brand = c("Own", "CompA", "CompB"),
    Share = shares
  )
  
  # ===========================================================================
  # 6. OPTIMAL PRICING & PROFIT MAXIMIZATION
  # ===========================================================================
  # Find price point that maximizes profit
  
  # Test price range from $1,500 to $2,600
  prices <- seq(1500, 2600, by = 100)
  
  # Calculate profit at each price point
  profits <- sapply(prices, function(p) {
    # Update price dummy based on threshold
    own_tmp <- own_design
    own_tmp["Price (low = 0; hi =1)"] <- ifelse(p >= 2500, 1, 0)
    
    # Recalculate utility with new price
    u_own_p <- partworth["(Intercept)"]
    for (feature in names(own_tmp)) {
      if (feature %in% names(partworth)) {
        u_own_p <- u_own_p + partworth[feature] * own_tmp[feature]
      }
    }
    
    # Calculate market share at this price
    u_all <- exp(c(u_own_p, u_A, u_B))
    share_p <- u_all[1] / sum(u_all)
    
    # Calculate profit
    cost <- sum(feature_costs[as.logical(own_tmp)])
    market_size <- 100
    margin <- p - cost
    sales <- share_p * market_size
    profit <- margin * sales
    
    return(profit)
  })
  
  # Identify optimal price and maximum profit
  optimal_price <- prices[which.max(profits)]
  max_profit <- max(profits)
  
  # ===========================================================================
  # 7. VISUALIZATIONS
  # ===========================================================================
  
  # Calculate market share at each price point
  shares_by_price <- sapply(prices, function(p) {
    own_tmp <- own_design
    own_tmp["Price (low = 0; hi =1)"] <- ifelse(p >= 2500, 1, 0)
    
    u_own_p <- partworth["(Intercept)"]
    for (feature in names(own_tmp)) {
      if (feature %in% names(partworth)) {
        u_own_p <- u_own_p + partworth[feature] * own_tmp[feature]
      }
    }
    
    u_all <- exp(c(u_own_p, u_A, u_B))
    return(u_all[1] / sum(u_all))
  })
  
  # Create side-by-side plots
  par(mfrow = c(1, 2))
  
  # Plot 1: Market Share vs Price
  plot(
    prices,
    shares_by_price,
    type = "l",
    main = "Market Share vs Price",
    xlab = "Price ($)",
    ylab = "Market Share",
    col = "blue",
    lwd = 2
  )
  abline(v = optimal_price, col = "red", lty = 2, lwd = 2)
  legend("topright", 
         legend = c("Market Share", "Optimal Price"),
         col = c("blue", "red"), 
         lty = c(1, 2),
         lwd = 2)
  
  # Plot 2: Profit vs Price
  plot(
    prices,
    profits,
    type = "l",
    main = "Profit vs Price",
    xlab = "Price ($)",
    ylab = "Profit ($)",
    col = "darkgreen",
    lwd = 2
  )
  abline(v = optimal_price, col = "red", lty = 2, lwd = 2)
  legend("topright",
         legend = c("Profit", "Optimal Price"),
         col = c("darkgreen", "red"),
         lty = c(1, 2),
         lwd = 2)
  
  # Reset plot parameters
  par(mfrow = c(1, 1))
  
  # ===========================================================================
  # 8. RETURN RESULTS
  # ===========================================================================
  
  return(list(
    Partworth_Table = partworth_table,
    Attribute_Importance = imp_table,
    Willingness_to_Pay = wtp_table,
    Market_Share = market_share,
    Optimal_Price = optimal_price,
    Maximum_Profit = max_profit
  ))
}

# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if (FALSE) {  # Set to TRUE to run example
  
  # Run analysis
  results <- conjoint_analysis(
    preferences_file = "data/Design_Matrix.xlsx",
    
    # Own product: Sony 4K 75" at low price
    own_design = c(
      "Resolution 4K = 1" = 1,
      "Sony = 1" = 1,
      "Price (low = 0; hi =1)" = 0,
      "Screen 75 inch" = 1,
      "Screen 85 inch" = 0
    ),
    
    # Competitor A: Sony 4K 75" at high price
    compA_design = c(
      "Resolution 4K = 1" = 1,
      "Sony = 1" = 1,
      "Price (low = 0; hi =1)" = 1,
      "Screen 75 inch" = 1,
      "Screen 85 inch" = 0
    ),
    
    # Competitor B: Non-Sony 4K 75" at low price
    compB_design = c(
      "Resolution 4K = 1" = 1,
      "Sony = 1" = 0,
      "Price (low = 0; hi =1)" = 0,
      "Screen 75 inch" = 1,
      "Screen 85 inch" = 0
    ),
    
    # Feature costs
    feature_costs = c(1000, 500, 1000, 250, 250)
  )
  
  # Display results
  cat("\n=== PART-WORTH UTILITIES ===\n")
  print(results$Partworth_Table)
  
  cat("\n=== ATTRIBUTE IMPORTANCE ===\n")
  print(results$Attribute_Importance)
  
  cat("\n=== WILLINGNESS TO PAY ===\n")
  print(results$Willingness_to_Pay)
  
  cat("\n=== MARKET SHARE ===\n")
  print(results$Market_Share)
  
  cat("\n=== OPTIMIZATION RESULTS ===\n")
  cat(sprintf("Optimal Price: $%d\n", results$Optimal_Price))
  cat(sprintf("Maximum Profit: $%.2f\n", results$Maximum_Profit))
}
