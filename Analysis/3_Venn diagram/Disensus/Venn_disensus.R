# 1. Install and load required packages
if (!require("ggvenn")) install.packages("ggvenn")
library(ggvenn)

# 2. Load the data
df <- data.frame(
  ID = 1:33,
  F1 = c(-2, -1, 0, 2, 2, 0, 1, 0, 2, 4, -2, 1, 3, 2, 3, 4, -2, -4, -1, -1, -1, 1, 0, -2, 3, 1, -3, -4, 1, 0, -3, -3, -1),
  F2 = c(1, 1, -2, -1, 0, 3, 2, 4, -3, -1, -3, 2, 3, 4, -2, 3, 0, -4, -2, -2, 1, 2, 1, -3, 2, -1, -1, -4, 0, -1, 1, 0, 0),
  F3 = c(-2, -2, -3, 2, 0, 0, -2, -1, -1, -2, 1, 1, 3, 1, 2, -3, 0, -4, -1, 1, 2, 2, 3, -1, 4, 3, -3, -4, -1, 1, 0, 0, 4),
  F4 = c(-3, -2, -4, -2, -1, -2, 1, 0, 3, 3, 1, 0, 3, 4, -3, 2, 1, -4, 1, -2, 2, 4, 2, 0, 0, -1, -1, -1, -3, 2, -1, 0, 1)
)

# 3. Define disensus function using ±2 threshold
is_disensus <- function(scores, target_score) {
  any_opposite_extreme <- any((target_score >= 2 & scores <= -2) | (target_score <= -2 & scores >= 2))
  return(any_opposite_extreme)
}

# 4. Get disensus IDs for each factor
get_disensus_set <- function(df, target_col, all_cols) {
  others <- setdiff(all_cols, target_col)
  ids <- c()
  
  for (i in 1:nrow(df)) {
    target_score <- df[[target_col]][i]
    if (abs(target_score) >= 2) {
      other_scores <- unlist(df[i, others])
      if (is_disensus(other_scores, target_score)) {
        ids <- c(ids, df$ID[i])
      }
    }
  }
  unique(ids)
}

# 5. Generate sets for Venn diagram
cols <- c("F1", "F2", "F3", "F4")
sets <- setNames(lapply(cols, function(col) get_disensus_set(df, col, cols)), cols)

# 6. Plot the Venn diagram
your_plot <- ggvenn(
  sets,
  fill_color = c("#FFB3BA", "#BAE1FF", "#BAFFC9", "#FFFFBA"),
  show_elements = TRUE,
  stroke_size = 0.3,
  text_size = 4
)

# 7. Save the plot
ggsave("Venn_disensus.png", plot = your_plot, dpi = 500, width = 6, height = 4)

