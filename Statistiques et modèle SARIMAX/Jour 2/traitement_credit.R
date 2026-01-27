
# #############################
#
#  Traitement "Credit"
#  NEXA M2
#  27/01/2026
#
# #############################




# Revenu
# Revenu en 1 000 $
#
# Limite
# Limite de crédit
#
# Note
# Cote de crédit
#
# Cartes
# Nombre de cartes de crédit
#
# Âge
# Âge en années
#
# Éducation
# Nombre d'années d'études
#
# Sexe
# Un facteur avec des niveaux Mâle et Femelle
#
# Étudiant
# Un facteur avec des niveaux Non et Oui indiquant si l'individu était étudiant
#
#  Marié
# Un facteur avec des niveaux Non et Oui indiquant si l'individu était marié
#
# Origine ethnique
# Un facteur avec des niveaux afro-américains, asiatiques et caucasiens indiquant l'origine ethnique de l'individu
#
# Solde
# Solde moyen de la carte de crédit en $.


library(ISLR2)

data("Credit")


str(Credit)

revenu <- 1000 * Credit$Income * 0.84
limite_credit <- 1000 * Credit$Limit * 0.84
score <- Credit$Rating
nbcarte <- Credit$Cards
age <- Credit$Age
education <- Credit$Education
solde <- 1000 * Credit$Balance * 0.84

qrevenu <- cut(revenu, breaks = c(8690, 17646, 27817, 48275, 156774), labels=c("rev1", "rev2", "rev3", "rev4"))
#qrevenu <- cut(revenu, breaks = c(8000, 18000, 28000, 49000, 160000), labels=c("rev1", "rev2", "rev3", "rev4"))

qlimite_credit <- cut(limite_credit, breaks = c(718199, 2593920, 2882900, 4933110, 11686921),
                      labels=c("limite1", "limite2", "limite3", "limite4"))

qscore <- cut(score, breaks = c(0, 247.2, 344, 437.2, 1000), labels=c("score1", "score2", "score3", "score4"))
qnbcarte <- cut(nbcarte, breaks = c(0, 2, 3, 4, 10), labels=c("nbcarte 1-2", "nbcarte 3", "nbcarte 4", "nbcarte 5 et +"))
qage <- cut(age, breaks = c(20, 41.75, 56, 70, 100), labels=c("age1", "age2", "age3", "age4"))
qeducation <- cut(education, breaks = c(4, 11, 14, 16, 20), labels=c("edu1", "edu2", "edu3", "edu4"))
qsolde <- cut(solde, breaks = c(-1, 57750, 385980, 724920, 1679161), labels=c("solde1", "solde2", "solde3", "solde4"))



proprietaire <- factor(Credit$Own, levels = c("No", "Yes"), labels = c("non", "oui"))
etudiant <- factor(Credit$Student, levels = c("No", "Yes"), labels = c("non", "oui"))
marie <- factor(Credit$Married, levels = c("No", "Yes"), labels = c("non", "oui"))
region <- factor(Credit$Region, levels = c("East", "South", "West"), labels = c("Est", "Sud", "Ouest"))



df <- data.frame(revenu, limite_credit, score, nbcarte, age,
                 education, proprietaire, etudiant, marie, region, solde)

df.quali <- data.frame(qrevenu, qlimite_credit, qscore, qnbcarte, qage,
                       qeducation, proprietaire, etudiant, marie, region, qsolde)

df.quali.V2 <- data.frame(qnbcarte, qage, qscore,
                          qeducation, proprietaire, etudiant, marie, region)

summary(revenu)
summary(limite_credit)
summary(score)
summary(nbcarte)
summary(age)
summary(education)
summary(solde)

summary(df.quali)

summary(qrevenu)


# Affichage multivarié


library(FactoMineR)
library(factoextra)
library(explor)

mca.V1 <- MCA(df.quali)

fviz_mca_biplot(mca.V1,
                repel = TRUE,
                geom.ind = c("point"),
                #col.ind = df.quali$infarctus,  # Couleur des individues
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


mca.V2 <- MCA(df.quali.V2)
explor(mca.V2)


