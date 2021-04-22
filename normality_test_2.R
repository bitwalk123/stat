library(nortest)

# sample dataset
name.file <- "data_norm.csv"
data <- read.csv(name.file)$x
print(data)

# Shapiro-Wilk test
result.shapiro <- shapiro.test(data)
print(result.shapiro)

# Anderson-Darling test
result.anderson <- ad.test(data)
print(result.anderson)
