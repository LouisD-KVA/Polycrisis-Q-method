# 1. Install and load required package
if (!require("ggvenn")) install.packages("ggvenn")
library(ggvenn)

# 2. Load the data
df <- data.frame(
  ID = 1:33,
  F1 = c(-3, -1, -1, 2, 2, 1, 2, 0, 3, 4, -2, 1, 4, 3, 3, 4, -2, -4, -2, -1, -1, 2, 0, -3, 3, 1, -4, -4, 1, 0, -3, -3, -2),
  F2 = c(1, 2, -3, -2, -1, 4, 2, 4, -3, -1, -3, 2, 3, 4, -2, 3, 0, -4, -2, -3, 2, 3, 1, -4, 3, -2, -1, -4, 0, -1, 1, 1, 0),
  F3 = c(-3, -3, -3, 3, 1, 0, -2, -1, -2, -2, 1, 1, 4, 2, 2, -3, 0, -4, -1, 1, 2, 3, 3, -2, 4, 3, -4, -4, -1, 2, -1, 0, 4),
  F4 = c(-3, -3, -4, -2, -2, -2, 2, 0, 3, 4, 1, 0, 3, 4, -3, 2, 1, -4, 2, -3, 3, 4, 2, -1, 0, -1, -1, -2, -4, 3, -1, 1, 1)
)

# 3. Define consensus function
is_consensus <- function(scores) {
  all_agree <- all(scores >= 3)
  all_disagree <- all(scores <= -3)
  range_ok <- max(scores) - min(scores) <= 1
  (all_agree || all_disagree) && range_ok
}

# 4. Get consensus IDs for a single target factor
get_consensus_set <- function(df, target_col, all_cols) {
  others <- setdiff(all_cols, target_col)
  ids <- c()
  
  for (other in others) {
    for (i in 1:nrow(df)) {
      scores <- c(df[[target_col]][i], df[[other]][i])
      if (is_consensus(scores)) {
        ids <- c(ids, df$ID[i])
      }
    }
  }
  unique(ids)
}

# 5. Generate sets for Venn
cols <- c("F1", "F2", "F3", "F4")
sets <- setNames(lapply(cols, function(col) get_consensus_set(df, col, cols)), cols)

# 6. Plot the Venn diagram and assign it to an object
your_plot <- ggvenn(
  sets,
  fill_color = c("#FFB3BA", "#BAE1FF", "#BAFFC9", "#FFFFBA"),
  show_elements = TRUE,
  stroke_size = 0.3,
  text_size = 4
)

# 7. Save the plot to file
ggsave("Venn.png", plot = your_plot, dpi = 500, width = 6, height = 4)