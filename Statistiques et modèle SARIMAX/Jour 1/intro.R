x <- rnorm(100)
hist(x)
summary(x)

head(x, n = 10)
head(x)
tail(x)

resume <- summary(x)

ma_moyenne <- sum(x) / length(x)
mean(x)

round(ma_moyenne, 6)

variance <- sum((x - mean(x))^2) / (length(x) - 1)
ET <- sqrt(variance)

var(x)
sd(x)

f_resume <- function(x){
  moyenne <- mean(x)
  variance <- var(x)
  ecart.type <- sd(x)
  
  cat("La moyenne est de ", moyenne, "\n")
  cat("La variance est de ", variance, "\n")
  cat("L'écart type est de ", ecart.type, "\n")
  
  hist(x)
}

f_resume(x)

y <- runif(1000)
f_resume(y)

hist(x)
hist(x, main = "TEST Histogramme", col = "lightblue")

#
# Graphique sous ggplot2
#

library(ggplot2)

df <- data.frame(x)

mygraph <- ggplot(df, aes(x)) +
  geom_histogram(color= "lightblue")

mygraph

# Boxplot

boxplot(x)


mygraph2 <- ggplot(df, aes(x)) 

mygraph2 + geom_boxplot()

hist(x)

x1 <- seq(1: 20)
y1 <- 2 + 3 * x1 + 20 * rnorm(20)

plot(y1 ~ x1,
     type = "b",
     pch=18,
     cex = 2,
)

# Nuage de points avec ggplot2

df3 <- data.frame(x1, y1)

mygraph3 <- ggplot(df3, aes(x1, y1)) + 
  geom_point()

mygraph3

# Modélisation 

x2 <- rnorm(20)
x3 <- runif(20)

plot(y1 ~ x1)
plot(y1 ~ x2)
plot(y1 ~ x3)

model.1 <- lm(y1 ~ x1 + x2 + x3)
summary(model.1)

model.2 <- lm(y1 ~ x1)
summary(model.2)

prev.2 <- model.2$fitted.values

plot(y1 ~ x1)
lines(prev.2 ~ x1)

acf(model.2$residuals)
hist(model.2$residuals)
