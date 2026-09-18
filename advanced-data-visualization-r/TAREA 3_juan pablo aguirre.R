library(dplyr)
require(readr)
library(reshape2)
library(astsa)
require(reshape2)
library(ggplot2)
########################################################################
# PREGUNTA 1
#######################################################################


covid=read.csv("C:/Users/Juan Pablo Aguirre/Desktop/Universidad Católica/2020_semestre_1/methods  EXPLORATORIOS estadística/clases/tarea 3/covid.csv", sep=";")

#covid = read.csv(github_covid_cl)

covid.rm <- melt(covid, id=c('Region'))  %>%
  filter(Region=='Metropolitana') %>%
  mutate(date=as.Date(variable, format = "X%d.%m.%Y")) %>%
  select(c("date","value"))

library(ggfortify)
datos<- ts(data = covid.rm$value, frequency=7)
#help(ts)
autoplot(decompose(datos, type = c("multiplicative")))


# los datos no son estacionales.
#####################################################################
# PREGUNTA 2
#####################################################################
#R: función de autocorrelación simple acf y autocorrelación 
parcial pacf.
acf(datos)
# Vemos que esta serie es no estacionaria , por que según se ve decrece
# muy lentamente , donde vemos muchos resagos son significativos, por
# lo tanto cuando vemos una serie de autocorrelograma de este estilo
# quiere decir que es "no estacionaria" y en definitivamente
# no es autocorrelacionada (por que decrece muy lentamente).
##################################################################
pacf(datos)
# Aquí vemos que tiene un resagos significativo muy visible, no sólo
# refireiendonos a la primera barra, como vemos que 5 barras alcanzan a 
# sobresalir del margen decimos que el modelo es autocorrelacionado
# de orden 6, pero este analisis se puede omitir, puesto que 
# en el análisis de autocorrelación es estacionario, aún teniendo
# resagos importantes.
# En definitiva que una persona muera no dependa de que otra haya
# muerto, según este análisis de autocorrelación del covid-19 en
# la región metropolitana.
###################################################################
# PREGUNTA 3
###################################################################
require(graphics)
#method = pgram y method = ar
#spectrum

spectrum(datos, method="pgram", plot=T)

spectrum(datos, method="ar", plot=T)


#################################################################
# PREGUNTA 4
require(graphics)
###############################################################
plot(stl(nottem, "per"))
plot(stl(nottem, s.window = 7, t.window = 50, t.jump = 1))
#Las mediciones en la figura 1 fueron realizadas por la Marina 
#de los EE. UU. Nacional Oceánica y Atmosféricaadministración,
#o NOAA, como parte de un programa gubernamental mundial para 
#monitorear concentraciones de CO2. Las mediciones abarcan el
#período del 17 de abril de 1974 al 31 de diciembre de 1986. 
#Eliminamos todas las ocurrencias del 29 de febrero, como si 
#ese día no existiera, para mantener el período igual a 365 días;
#así los datos, con estos días eliminados, sapn 4609 dias. 
#Faltan datos para 416 de estos días, por lo que en total hay
#4193 mediciones de CO2.
#Los datos, graficados en el primer panel (superior), son promedio diario
#mediciones de dióxido de carbono atmosférico (CO2) realizadas en el
#Observatorio Mauna Loa en Hawai. El segundo panel grafica un
#componente de tendencia: la variación de baja frecuencia en los datos
#junto con cambios de nivel no estacionarios a largo plazo.
#El tercer panel grafica un componente estacional: variación en
#los datos en o cerca de la frecuencia estacional, que en este
#caso en un ciclo por año. El componente restante, mostrado
#en el cuarto panel, es la variación restante en los datos
#más allá de eso en el componente estacional y de tendencia.
#Es decir, supongamos los datos, el componente de tendencia, 
#el componente estacional, y el componente restante se denota por
#Y_ {v}, T_ {v}, S_ {v} y R_ {v}, respectivamente:
#Y_ {v} = T_ {v} + S_ {v} + R_ {v}
#############################################################

#Aquí, el gráfico de descomposición, muestra los datos y
#trhee componentes El marco temporal de los rangos de datos.
#desde Janaury 1959 hasta diciembre de 1987; esto fue todo
#los datos disponibles de nuestra fuente, el carbono
#Centro de análisis de información sobre dióxido de Oak Ridge
#Laboratorio Nacional, en el momento en que nuestro análisis fue
#llevado a cabo. Hay una periodicidad anual, entonces n_ {p} = 12.

plot(stllc <- stl(log(co2), s.window = 21))
# acá se muestra un resumen por cada desocmposición.
summary(stllc)
## linear trend, strict period.
plot(stl(log(co2), s.window = "per", t.window = 1000))

## Two STL plotted side by side :
        stmd <- stl(mdeaths, s.window = "per") # non-robust
summary(stmR <- stl(mdeaths, s.window = "per", robust = TRUE))
op <- par(mar = c(0, 4, 0, 3), oma = c(5, 0, 4, 0), mfcol = c(4, 2))
plot(stmd, set.pars = NULL, labels  =  NULL,
     main = "stl(mdeaths, s.w = \"per\",  robust = FALSE / TRUE )")
plot(stmR, set.pars = NULL)
# mark the 'outliers' :
(iO <- which(stmR $ weights  < 1e-8)) # 10 were considered outliers
sts <- stmR$time.series
points(time(sts)[iO], 0.8* sts[,"remainder"][iO], pch = 4, col = "red")
par(op)   # reset

###############################################################
# PREGUNTA 5 model 2 with outliers
###############################################################
load("C:/Users/Juan Pablo Aguirre/Desktop/Universidad Católica/2020_semestre_1/methods  EXPLORATORIOS estadística/clases/tarea 3/growth.rda")
growth <- na.omit(growth)

## data_base
load("C:/Users/Juan Pablo Aguirre/Desktop/Universidad Católica/2020_semestre_1/methods  EXPLORATORIOS estadística/clases/tarea 3/growth.rda")
growth <- na.omit(growth)

#fbplot para niñas
fbplot(growth$hgtf ,method='MBD', xlim=c(1,18),
       ylim=c(min(growth$hgtf),max(growth$hgtf)),
       xlab= "edad de niñas" ,ylab="altura de niñas (cm)",
       main= "Gráfico de altura de niñas v/s su edad") 



#Observación: recordando lo que vimos en clases, un corte transversal
#representa un boxplot, dentro de ello en la zona morada (rosada) 
#vemos intervalos intercualtiles, cuyos límites de la linea azul
#son los puntos mínimos y máximos, y por último la linea punteada
#que alcanzamos a ver representan los datos atípico u outliers.

#En este caso (de las niñas), vemos que a la edad de 5 años se ve una dispersion 
#entre el primer cuartil y la mediana. A medida que avanzamos en la
#edad media, la altura en (cm) aumento  en unos 40 (cm)entre los 5
#y los 15 años. En general en todo el transcurso entre 1 y 18 años
#no se ven difernecias de dispersion en la altura (cm) entre el
#primer cuartil y la mediana. En definitiva, todos los resumenes 
#estadísticos de los cortes transversales de Boxplot van aumentando
#a medida que  avanzamos en la edad la edad aumenta en las niñas.



#fbplot para niños
fbplot(growth$hgtm ,method='MBD', xlim=c(1,18),
       ylim=c(min(growth$hgtm),max(growth$hgtm)),
       xlab= "edad de niños" ,ylab="altura de niños (cm)",
       main= "Gráfico de altura de niños v/s su edad")


# Entre 1 y 5 años hay mayor dispersión de edad entre en los
#cuartiles 1 y 2 , mientras que hay más concentración de datos entre 
#el cuartil 2 y 3. 

#Una diferecia principal entre niñas y niños, es que las primeras
#tienen datos atípicos. Y otra bien notoria , es que en rangos
#de edad similar las niñas tienen una mayor estatura (cm).
#Similarmente, ambos niños y niñas crecen a medida que aumenta
#la edad entre los 1 y 18 años.

mean(growth$hgtf)
mean(growth$hgtm)
# De ambas muestras, sabemos que la media muestral no esun buen medidor
# pero aun así y viendo los gráficos, la media de estatura de las
# niñas es mayor a la de los niños. Y las niñas presnetan datos 
# atípicos en comparación a los niños que no se visualizan.
###############################################################
# PREGUNTA 6
###############################################################

library(reshape2)
library(ggplot2)
hgtf<- melt(growth$hgtf[,1:10])

ggplot(data= hgtf, aes(x= Var1, y = value, group= Var2))+geom_line()+
           ggtitle("Plot spaguetti, de las 10 primeras niñas") +
           xlab("edad en (años)") + ylab("Altura en cm.")+
          theme(
plot.title = element_text(color="red", size=14, face="bold.italic"),
axis.title.x = element_text(color="blue", size=14, face="bold"),
axis.title.y = element_text(color="#993333", size=14, face="bold")
)


# es otra alternativa para ver el crecimiento (cm) en relación a 
#la edad de un grupo de las  10 primeras niñas del archivo growth.
#Veamos como la altura (cm) de las 10 niñas se estanca después de
#los 15 años.





