# TAREA 2

orders <- read.csv("C:/Users/Juan Pablo Aguirre/Desktop/Universidad Católica/2020_semestre_1/methods en estadísitica exploratoria/clases/tarea 2/Tarea_2/orders.csv")
head(orders)
##############
# EJERCICIO 1
##############
library(ggplot2)
library(ggmosaic)

x1<- orders$Segment
x2<- orders$State
ggplot(data=orders) + geom_mosaic(aes(x=product(x1,x2), fill=x1)) + labs(x="State", y="Segment")

# Invertido tenemos:

ggplot(data=orders) + geom_mosaic(aes(x=product(x2,x1), fill=x2)) + labs(x="Segment", y="State", title= "Segment v/s State")
#############
# EJERCICIO 2
#############
# https://stackoverflow.com/questions/1296646/how-to-sort-a-dataframe-by-multiple-columns
newdata <- orders[order(orders$Sales),]
datanew<- newdata[newdata$Sales>400 & newdata$Sales < 4000,]
x<- datanew$Sales
y<- datanew$Profit
n<- length(x)

dta <- data.frame(x=x, y=y)

# Scatterplot
require(ggplot2)
( p0 <- ggplot(dta, aes(x, y)) + geom_point() + ggtitle("Scatterplot") + labs(x="Sales", y="Profit", title= "Profit v/s Sales"))
# Linear regression
( p1 <- p0 + geom_smooth(method="lm", formula=y~x, se=F, color="black") )
# Polynomial regression of degree 2
( p2 <- p1 + geom_smooth(method="lm", formula=y~poly(x,2), se=F, color="green") )
# Polynomial regression of degree 3
( p3 <- p2 + geom_smooth(method="lm", formula=y~poly(x,3), se=F, color="cornflowerblue") )


######################################################
#              LOESS IMPLEMENTATION                  #
######################################################
# Smoothing parameter or degree of smoothing
span <- 0.1
# number of points for local regression
n.pts <- ceiling(nrow(dta)*span)
# Prediction with LOESS
prediction <- rep(NA,nrow(dta))

for(i in 1:nrow(dta)){
    # Position of each pair (X,Y) and the distance of each X in relation to Xi
    aux <- data.frame(pos=1:nrow(dta),dist=abs(dta$x[i]-dta$x))
    # Position of the n.pts closest points to Xi
    pos <- aux[order(aux$dist),]$pos[1:n.pts]
    # Distance between Xi and each of the n.pts selected points
    dist <- aux[order(aux$dist),]$dist[1:n.pts]
    # Scaled distance
    scl.dist <- dist/max(dist)
    # Tricube weight function
    w <- (1-abs(scl.dist)^3)^3
    # Points for local regression
    x <- dta$x[pos]
    y <- dta$y[pos]
    # Weighted Linear polynomial regression
    model <- lm(y ~ x, weights=w)
    # Prediction for Yi
    prediction[i] <- predict(model, newdata=data.frame(x=dta$x[i]))
}

# Plotting the loess curve implemented manually
( p4 <- p3 + geom_line(aes(y=prediction),col="darkgoldenrod1",cex=1) )
######################################################


# LOESS regression of degree 1 (span=0.1)
( p5 <- p4 + geom_smooth(method="loess", formula=y~x, span=0.1, method.args=list(degree=1), se=F, col="green") )
# LOESS regression of degree 1 (span=0.5)
( p6 <- p5 + geom_smooth(method="loess", formula=y~x, span=0.5, method.args=list(degree=1), se=F, col="darkolivegreen4") )
# LOESS regression of degree 1 (span=0.8)
( p7 <- p6 + geom_smooth(method="loess", formula=y~x, span=0.8, method.args=list(degree=1), se=F, col="darkgreen") )
# LOESS regression of degree 2 (span=0.1)
( p8 <- p7 + geom_smooth(method="loess", formula=y~x, span=0.1, method.args=list(degree=2), se=F, col="brown1") )

# A medida que los grados del polinomio iban aumentando,
# a travez de la regresion de LOESS se iba ajustando de mejor 
# forma a los datos de de Profit , en ventas entre
# $400 y $4000 dólares.


#La regresión LOESS es una técnica no paramétrica que utiliza la
#regresión ponderada local para ajustar una curva suave a través
#de puntos en un diagrama de dispersión.


#############
# EJERCICIO 3
#############
H<- orders[,c("State", "City" , "Sales", "Profit", "Discount")]
#head(H)
library(dplyr)
H.Florida = subset(H,State=="Florida") 
H.new3<- H[,-1]
head(H.new3)
Resumen<- summary(H.new3)  

Resumen + summarise(n= sum(Sales, na.rm = TRUE)
