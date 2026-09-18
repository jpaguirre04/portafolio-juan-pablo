library(dplyr)
library(gapminder)
data(gapminder)
#head(gapminder)


###############################################################
# EJERCICIO 1
###############################################################

dta1 <- gapminder %>% group_by(year) %>% summarise(y=sum(gdpPercap)) %>% 
		rename(t= year)

par(mar=c(4,4,2,0.5))
plot(dta1$t, dta1$y, type="l", col="red2", xlab="Años en decenios", ylab="gdpPercap", cex.lab=0.7, 
	 main="Ingreso percápita gdpPercap", cex.main=0.9, font.main=4,
       sub="Primer gráfico de la primera tarea", cex.sub=0.7,las=1)
points(dta1$t, dta1$y, pch=24, col="red2", bg="seagreen2", bty="7")
legend("bottomright", legend="time series", title="legend", col="red2", lty=1, pch=19, inset=.01)


###############################################################
# EJERCICIO 2
###############################################################
require(ggplot2)
# ggplot2

dta1$obj <- "Ejercicio 2- gdpPercap" 
ggplot(dta1, aes(x=dta1$t, y=dta1$y, color=obj)) + 
       geom_line(color = "#00AFBB", size = 2)+ 
       geom_point(colour = "red", size = 4) +
       labs(x="Años: 1952-2007",y="Ingreso Per cápita") +
       ggtitle("Ejercicio 2, gdpPercap") + theme(plot.title=element_text(hjust=0.5)) +
       labs(color="legend") + theme(legend.position=c(0.92,0.07)) 


###############################################################
# EJERCICIO 3
###############################################################

library(dplyr)
library(gapminder)
data(gapminder)
# continente europeo
dataeu <- gapminder %>% filter(continent=="Europe")
myfun.boxplot <- function(x,...){
 boxplot(x,...)
}
myfun.boxplot(dataeu$lifeExp,main="Expectativa de Vida en Europa",col="yellow",
                      xlab= "Expectativa")
              legend("bottomleft", legend = "Continente Europeo")


#Los valores atípicos que se ven en esta muestra, pueden ser 
#indicativos de datos que pertenecen a una población diferente 
#(población inmigrante) del resto de las muestras establecidas.
#Puesto que en otros continentes las expectativas son más bajas
# en comparación a Europa.

###############################################################
# EJERCICIO 4
###############################################################
#library(openxlsx)
#library(readxl)

#Gaussian
Kernel <- function(u) exp(-1/2*u^2)/sqrt(2*pi)
fhat <- function(y) mean(Kernel((y-dat$x)/h)/h)
v.fhat <- function(y) sapply(y,fhat)


#epanechnikov
KernelE <- function(u) (3/4)*(1-u^2)
fhatE <- function(z) mean(KernelE((z-dat$x)/h)/h)
v.fhatE <- function(z) sapply(z,fhatE)


setwd("C:/Users/Juan Pablo Aguirre/Desktop/Universidad Católica/2020_semestre_1/method/clases/tarea 1")
dat <- read.table("Puntajes.txt", sep=" ",header=TRUE)
n<- length(dat$x)
summary(dat)

# Histogram
hist(dat$x, prob=T, main="Gaussiana vs Epanechnikov", xlab="elementos", ylab="puntaje", breaks=30)

# Silverman's rule of thumb for the bandwidth= Regla de Silverman del ancho
# de banda.
h <- 0.9*min(sd(dat$x),IQR(dat$x)/1.34)*n^(-1/5)

#summary(dat$x)

##############################################
# Points evaluated at our Gaussian kernel
#y <- seq(100,400,len=500)
#lines(y, v.fhat(y), col="red")


# Points evaluated at our Gaussian kernel
#z <- seq(100,400,len=500)
#lines(z, v.fhatE(z), col="yellow")
###############################################

# Density plot using Gaussian
lines(density(dat$x, kernel="gaussian"), col="red")

# Density plot using Epanechnikov
lines(density(dat$x, kernel="epanechnikov"), col="green")


# Errores cuadráticos medios
Error2medioGauss<- sum(density(dat$x, kernel="gaussian")$x - mean(dat$x))/length(density(dat$x, kernel="gaussian")$x)
Error2medioGauss
Error2medioepanechnikov<- sum(density(dat$x, kernel="epanechnikov")$x - mean(dat$x))/length(density(dat$x, kernel="epanechnikov")$x)
Error2medioepanechnikov


# Hasta desde x=120.6 hasta antes de x=350 de la muestra , se observa
la misma aproximación de ambos métodos a los calores reales.
# En cambio de x=350 hacia adelante el método Epanechnikov presenta
# mejor aproximación a los datos reales  que el método Gaussiano. Sin embargo,
# en cuanto a los valores de errores cuadráticos medios, ambos no presentaron
# diferencias entre sí.



###############################################################
# EJERCICIO 6
###############################################################
#library(openxlsx)
#library(readxl)
# Library
install.packages("ggplot2", dependencies = TRUE)
install.packages('Rcpp', dependencies = TRUE)
library(ggplot2)

# caso de cáncer de mama

setwd("C:/Users/Juan Pablo Aguirre/Desktop/Universidad Católica/2020_semestre_1/method/clases/tarea 1")
dat6.5<- read.table("cancermama.txt", sep=",",header=TRUE,fill = TRUE)
head(dat6.5)

##########################################################
# PEQUEÑOS ENTREAMIENTOS
##########################################################

# violin plot with dot plot
p + geom_dotplot(binaxis='y', stackdir='center', dotsize=1)
# violin plot with jittered points
# 0.2 : degree of jitter in x direction
p + geom_jitter(shape=16, position=position_jitter(0.2))


# Change violin plot line colors by groups
p<-ggplot(dat6.5, aes(x= diagnosis, y=radius_mean, color=diagnosis)) +
  geom_violin(trim=FALSE)
p


# Use single color
ggplot(dat6.5, aes(x= diagnosis, y=radius_mean)) +
  geom_violin(trim=FALSE, fill='#A4A4A4', color="darkred")+
  geom_boxplot(width=0.1) + theme_minimal()
  geom_dotplot(binaxis='y', stackdir='center', dotsize=1)


#############################################################################
# Comparaciones entre el radio, perimetro y área , ojo que estas tres últimas
# variantes tienen rangos y unidades de medida diferentes, perímetro y área.
# provinen de la medición del radio del núcleo celular. Las mediciones
# son del "Núlceo Celular".
############################################################################


# Radio-Change violin plot colors by groups
p<-ggplot(dat6.5, aes(x= diagnosis, y=radius_mean, fill=diagnosis)) +
  geom_violin(trim=FALSE) +
  geom_violin(trim=FALSE, fill='#A4A4A4', color="darkred")+
  geom_boxplot(width=0.1) + theme_minimal()+
  geom_jitter(shape=16, position=position_jitter(0.2))+
  labs(title="Radio celular vs diagnosis",x="Diagnosis (M = malignant, B = benign)", y = "radius_mean")
p


#Perimetro-Change violin plot colors by groups
p<-ggplot(dat6.5, aes(x= diagnosis, y=perimeter_mean, fill=diagnosis)) +
  geom_violin(trim=FALSE) +
  geom_violin(trim=FALSE, fill='#A4A4A4', color="darkred")+
  geom_boxplot(width=0.1) + theme_minimal()+
  geom_jitter(shape=16, position=position_jitter(0.2))+
  labs(title="Perímetro celular vs diagnosis",x="Diagnosis (M = malignant, B = benign)", y = "perimeter_mean")
p


#Perimetro-Area violin plot colors by groups
p<-ggplot(dat6.5, aes(x= diagnosis, y=area_mean, fill=diagnosis)) +
  geom_violin(trim=FALSE) +
  geom_violin(trim=FALSE, fill='#A4A4A4', color="darkred")+
  geom_boxplot(width=0.1) + theme_minimal()+
  geom_jitter(shape=16, position=position_jitter(0.2))+
  labs(title="Area celular vs diagnosis",x="Diagnosis (M = malignant, B = benign)", y = "area_mean") 
p


#############
#Observación
#############
# En los 3 casos anteriores de los violin-boxplot la media 
# de ambas variantes (radio, perímetro y área) la media de las celulas 
# malignas es más predominante en relacion a las celulas Benignas.

# Además en los 3 casos de (radio, perímetro y área) las células 
# Malignas presentan datos mucho más dispersos en relación
# a las células malignas.

# Los datos del área celular Maligna presentan más dispersión
# En las 3 mediciones las células Benignas tienen más agrupamiento.

#Motivación: existe el área y el perímetro para trabajar en esta descripción
# de los datos pero el radio es importante ya que el mismo entrega la información
# de sí misma y las otras dos restantes.

# NO se visualiza diferencias patentes entre el radio y perímetro.
##########################################################################

#########################################################################
# Una variante importante en los estudios de bioquímica profesor
# es la asimetría en una célula cancerígena, ya que la estructura
# de una de ellas es amorfa, de modo que analizaré qué diferencia
# descriptiva visual en violin-boxplot de la symmetry_worst (peor-simetría).



# Radio-Change violin plot colors by groups
p<-ggplot(dat6.5, aes(x= diagnosis, y=symmetry_worst, fill=diagnosis)) +
  geom_violin(trim=FALSE) +
  geom_violin(trim=FALSE, fill='#A4A4A4', color="darkred")+
  geom_boxplot(width=0.1) + theme_minimal()+
  geom_jitter(shape=16, position=position_jitter(0.2))+
   labs(title="Peor simetría de células cancerígenas",x="Diagnosis (M = malignant, B = benign)", y = "Peor Simetría") 
p

dp <- ggplot(dat6.5, aes(x= diagnosis, y=symmetry_worst, fill=diagnosis)) + 
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(title="Peor simetría de células cancerígenas",x="Diagnosis (M = malignant, B = benign)", y = "Peor Simetría")
dp + theme_classic()

#############
#Observación
#############
# En la células Malignas existe una dispersión de datos entre la Mediana
# y el tercer Cuartil(Q3), por ello se puede visulaizar un sesgo, en comparación
# a las células Benignas (que se nota simétrica en relación a una asimetría). 
#Por lo tanto, hay datos dispersos de las células Malignas que tienden a tener
#una asimetría muy gigantezca.



#####################################################################
# Bibliografía!!!!
#Las características se calculan a partir de una imagen digitalizada 
#de un aspirado con aguja fina (FNA) de una masa mamaria. Describen 
#las características de los núcleos celulares presentes en la imagen.
#n el espacio tridimensional es el descrito en: [K. P. Bennett y O. L.
#Mangasarian: "Discriminación de programación lineal robusta de dos conjuntos 
#inseparables linealmente", Optimization Methods and Software 1, 1992, 23-34].

#Esta base de datos también está disponible a través del servidor ftp UW CS:
#ftp ftp.cs.wisc.edu
#cd math-prog / cpo-dataset / machine-learn / WDBC /




##################################################################################
# Violin plot Profesor Danilo.
ggplot(dat6.5, aes(x= diagnosis, y=radius_mean, fill=diagnosis)) + geom_violin() + xlab("diagnosis") + ylim(-5,55) +
  theme(axis.text.x=element_blank(),axis.ticks.x=element_blank(),legend.position="none") +
  ggtitle("Violin plot")
#################################################################################





