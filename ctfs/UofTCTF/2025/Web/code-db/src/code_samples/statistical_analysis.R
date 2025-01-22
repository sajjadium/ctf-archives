# Load libraries
library(dplyr)
library(ggplot2)

# Generate sample data
set.seed(123)
data <- data.frame(
    group = rep(c("A", "B", "C"), each = 100),
    value = c(rnorm(100, mean=50, sd=10),
              rnorm(100, mean=60, sd=15),
              rnorm(100, mean=55, sd=12))
)

# Summary statistics
summary_stats <- data %>%
    group_by(group) %>%
    summarise(
        mean = mean(value),
        sd = sd(value),
        count = n()
    )

print(summary_stats)

# Visualization
ggplot(data, aes(x=group, y=value, fill=group)) +
    geom_boxplot() +
    theme_minimal() +
    ggtitle("Boxplot of Values by Group")
