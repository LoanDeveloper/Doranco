###########################
#
# Traitement infractus
#
###########################

# ---------------------------------------------------------
# 1 - Lecture des données et chargement des librairies
# ---------------------------------------------------------

# Chargement des librairies
library(gmodels)

# répertoire de travail
setwd("~/Bureau/cours/semaine-26-01-2026")

# lecture des données
df <- read.table("data_infarctus.csv", header = TRUE, sep = ";", dec = ".")

View(df)
head(df)
tail(df)

summary(df)

# -----------------------------
# 2 - Préparation des données
# -----------------------------

# 2.1 Variables quantitatives

age <- df$AGE
poids <- df$POIDS
tailles <- df$TAILLE

# 2.2 Variables qualitatives

infarctus <- factor(df$INFARCT, levels = c(0, 1), labels = c("non", "oui"))
contracpection <- factor(df$CO, levels = c(0, 1), labels = c("non", "oui"))
tabac <- factor(df$TABAC, levels = c(0, 1, 2), labels = c("non fumeur", "fumeur", "ancien fumeur"))
antecedent <- factor(df$ATCD, levels = c(0, 1), labels = c("non", "oui"))
hypertention <- factor(df$HTA, levels = c(0, 1), labels = c("non", "oui"))

# -----------------------------
# 3 - Analyse univariée
# -----------------------------

# 3.1 Variables quantitatives

hist(age)
summary(age)
sd(age)
boxplot(age)

hist(poids)
summary(poids)
sd(poids, na.rm = TRUE)
boxplot(poids)

hist(tailles)
summary(tailles)
sd(tailles)
boxplot(tailles)

# 3.2 Variables qualitatives

tab1 <- table(infarctus)
prop.table(tab1)
proportions(tab1)
CrossTable(infarctus)

table(tabac)
CrossTable(tabac)

table(contracpection)
CrossTable(contracpection)

table(antecedent)
CrossTable(antecedent)

table(hypertention)
CrossTable(hypertention)

plot(infarctus)
plot(tabac)
plot(contracpection)
plot(antecedent)
plot(hypertention)

# -----------------------------
# 4 - Analyse bivariée
# -----------------------------

# 4.1 Variables quanti vs infractus

qage <- cut(age, breaks = c(14, 33, 44, 56, 100), labels=c("age1", "age2", "age3", "age4"))
qpoids <- cut(poids, breaks = c(30, 51, 64, 79, 130), labels=c("poids1", "poids2", "poids3", "poids4"))
qtaille <- cut(taille, breaks = c(130, 160, 166, 171, 184), labels=c("taille1", "taille2", "taille3", "taille4"))
qimc <- cut(imc, breaks = c(0, 18.5, 25, 50), labels=c("imc_inf_18.5", "imc18.5_25", "imc_sup_25"))


df.quali <- data.frame(infarctus, contraception, antecedent, hypertension, tabac, qage, qimc)
df.quali <- na.omit(df.quali)

taux_train <- 0.8
indices <- sample(nrow(df.quali), nrow(df.quali) * taux_train)
df.train <- df.quali[indices, ]
df.test <- df.quali[-indices, ]

str(df.quali)
str(df.train)
str(df.test)



# Affichage multivarié


library(FactoMineR)
library(factoextra)
library(explor)

mca.V1 <- MCA(df.quali)

fviz_mca_biplot(mca.V1,
                repel = TRUE,
                geom.ind = c("point"),
                col.ind = df.quali$infarctus,  # Couleur des individues
                # col.ind = as.factor(groupe.kmeans),  # Couleur des individues
                alpha.ind = 0.3,
                geom.var = c("point", "text"),
                col.var = "black", # Couleur des variables
                # arrows = c(FALSE, TRUE),
                # pointsize = 1,
                shape.var = 15,
                size.var = 6,
                addEllipses = TRUE
)


explor(mca.V1) 