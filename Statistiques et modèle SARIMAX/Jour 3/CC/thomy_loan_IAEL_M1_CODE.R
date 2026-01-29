#############################
#  CC - CREDIT
#  Statistiques & SARIMAX (partie Stats / ML)
#  NEXA M2 - Janvier 2026
#############################

# -----------------------------
# 0) Librairies
# -----------------------------
# Installer au besoin :
install.packages(c("gmodels","DescTools","MASS","caret","pROC","randomForest"))

library(gmodels)     # CrossTable
library(DescTools)   # CramerV
library(MASS)        # stepAIC
library(caret)       # split + confusionMatrix
library(pROC)        # ROC/AUC
library(randomForest)

# -----------------------------
# 1) Chargement des données
# -----------------------------
setwd("/mnt/data/Documents/Doranco/Statistiques et modèle SARIMAX/Jour 3")

df0 <- read.table("data_credit.csv", header = TRUE, sep = ";", dec = ".", strip.white = TRUE)

# 1.2 Structure
str(df0)

# 1.3 Intitulés + nb colonnes + nb lignes
names(df0)
ncol(df0)
nrow(df0)
dim(df0)

# 1.4 4 premiers + 4 derniers individus
head(df0, 4)
tail(df0, 4)

# -----------------------------
# 2) Préparation des données
# -----------------------------
# 2.1 Variables quanti/quali (avant conversion)
# Quanti attendues : age, revenu, probleme
# Quanti codées mais qualitatives : proprietaire, independant, acceptation

# 2.2 Conversion "bon escient"
age <- as.numeric(df0$age)
revenu <- as.numeric(df0$revenu)
probleme <- as.numeric(df0$probleme)

proprietaire <- factor(df0$proprietaire, levels = c(0, 1), labels = c("non", "oui"))
independant  <- factor(df0$independant,  levels = c(0, 1), labels = c("non", "oui"))
acceptation  <- factor(df0$acceptation,  levels = c(0, 1), labels = c("non", "oui"))

# 2.3 Data frame final
df <- data.frame(age, revenu, proprietaire, independant, probleme, acceptation)

# 2.4 Vérif structure
str(df)
summary(df)

# -----------------------------
# 3) Analyse descriptive
# -----------------------------
# 3.1 Variable cible
# acceptation

# 3.2-3.3 Quali vs cible : tableau, pourcentages, Khi2, V de Cramér
CrossTable(df$acceptation)

for (v in c("proprietaire", "independant")) {
  cat("\n====================\nVariable:", v, "\n")
  tab <- table(df[[v]], df$acceptation)
  print(tab)
  print(prop.table(tab, margin = 1))  # taux par modalité de v
  
  # Khi2 + V de Cramér
  chi <- chisq.test(tab)
  print(chi)
  
  # V de Cramér (0 à 1)
  cat("Cramer V =", CramerV(tab), "\n")
}

# 3.4-3.5 Quanti vs cible : stats par groupe + tests + graph
for (v in c("age", "revenu", "probleme")) {
  cat("\n====================\nVariable:", v, "\n")
  print(by(df[[v]], df$acceptation, summary))
  print(by(df[[v]], df$acceptation, sd))
  
  # Graph
  boxplot(df[[v]] ~ df$acceptation, main = paste("Boxplot", v, "par acceptation"),
          xlab = "acceptation", ylab = v)
  
  # Test t de Welch (souvent utilisé), et Wilcoxon en alternative
  print(t.test(df[[v]] ~ df$acceptation))
  print(wilcox.test(df[[v]] ~ df$acceptation))
}

# -----------------------------
# 4) Modèle logistique
# -----------------------------
# 4.1 Split 70/30
set.seed(123)
idx_train <- createDataPartition(df$acceptation, p = 0.70, list = FALSE)
dftrain <- df[idx_train, ]
dftest  <- df[-idx_train, ]

# 4.2-4.3 Modèle logistique (glm binomial)
m_full <- glm(acceptation ~ age + revenu + proprietaire + independant + probleme,
              data = dftrain, family = binomial)
summary(m_full)

# 4.4 Choix modèle : AIC / stepwise (exemple)
m_step <- stepAIC(m_full, direction = "both", trace = FALSE)
summary(m_step)
AIC(m_full, m_step)

# 4.5 Interprétation : OR (odds ratios)
coef_table <- cbind(
  coef = coef(m_step),
  OR = exp(coef(m_step)),
  confint.default(m_step) # IC approx
)
coef_table

# -----------------------------
# 5) Évaluation du modèle
# -----------------------------
# 5.1-5.2 Prédictions proba + classes
proba_test <- predict(m_step, newdata = dftest, type = "response")
pred_test <- ifelse(proba_test >= 0.5, "oui", "non")
pred_test <- factor(pred_test, levels = c("non", "oui"))

head(proba_test)
head(pred_test)

# 5.3 Matrice de confusion
confusionMatrix(pred_test, dftest$acceptation, positive = "oui")

# Bonus : ROC/AUC
roc_obj <- roc(response = dftest$acceptation, predictor = proba_test, levels = c("non","oui"))
auc(roc_obj)
plot(roc_obj, main = "ROC - Régression logistique")

# -----------------------------
# 6) Amélioration : randomForest
# -----------------------------
set.seed(123)
rf <- randomForest(acceptation ~ age + revenu + proprietaire + independant + probleme,
                   data = dftrain, ntree = 500, mtry = 2, importance = TRUE)

rf

pred_rf <- predict(rf, newdata = dftest, type = "class")
confusionMatrix(pred_rf, dftest$acceptation, positive = "oui")

proba_rf <- predict(rf, newdata = dftest, type = "prob")[, "oui"]
roc_rf <- roc(response = dftest$acceptation, predictor = proba_rf, levels = c("non","oui"))
auc(roc_rf)
plot(roc_rf, main = "ROC - RandomForest")

importance(rf)
varImpPlot(rf)
