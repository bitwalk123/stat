library(nortest)
#library(goftest)

# sample dataset
data <- rnorm(150, mean = 20, sd = 5)
print(data)

# Shapiro-Wilk test
result <- shapiro.test(data)
print(result)

# Anderson-Darling test
result <- ad.test(data)
print(result)
