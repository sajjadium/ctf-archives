# Load necessary library
library(ggplot2)

# Sample data
data <- data.frame(
    category = c('A', 'B', 'C', 'D'),
    values = c(23, 17, 35, 29)
)

# Summary statistics
print(summary(data))

# Plot
ggplot(data, aes(x=category, y=values, fill=category)) +
    geom_bar(stat='identity') +
    theme_minimal() +
    ggtitle("Category Values")
