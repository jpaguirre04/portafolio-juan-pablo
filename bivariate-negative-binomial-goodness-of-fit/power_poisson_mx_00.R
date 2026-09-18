library(methods)
library(Runuran)
B_est<-function(a,b,c,datos_x,datos_y,N,v){
       p1<- (a - c)/(1+a+b-c)
       p2<- (b - c)/(1+a+b-c)
       p3<-  c/(1+a+b-c)
       q<-   1/(1+a+b-c)
       #print(c(p1,p2,p3,q))
       S<- matrix(0,N,N)
        suma<-0
         for(i in 1:N){
             for(j in 1:N){
                 S[i,j]<- 1/((datos_x[i]+datos_x[j]+1)*(datos_y[i]+datos_y[j]+1))
             }
          }
       B<- sum(S)/N
       i<- j <- 1:N
       k<- l <- m <- 0:(N-1)
       g<- function(k,l,m,p1,p2,p3,q,v,N){choose(k,l)*choose(k-l,m)* p1^(k-l-m) * p2^l *p3^m *(q^v *N*choose(2*v+k-1,k)*(1/((k-l+1)*(l+m+1)))-2* choose(v+k-1,k) *1/((datos_x[i]+k-l+1)*(datos_y[i]+l+m+1)))}
       J<- q^v * sum(outer(k,l,m,p1,p2,p3,q,v,N,FUN=g),na.rm=TRUE)
       TOT<- B+J
       return(TOT)                      
 }# fin de B_est
########################################################################################    
# metodo doble cero
########################################################################################
freczero<- function(a_0,a_1,tabla,N,v){
                         g_2<-  1+ a_0 + a_1 - (tabla[1,1]/ N)^(-1/v)
                        if(g_2 < 0 || tabla[1,1]== 0 || abs(g_2 - min(a_0 ,a_1))< .20778899) g_2 <- 0
                        return(g_2)
                 }
#############################################################################################
# metodo de maxima verosimilitud
#############################################################################################
     est.maxima<- function(datos_a,datos_b,a_0,a_1,a_2,N,v){#a_0,a_1,a_2,v,N son constantes.
                # ocupar como valores iniciales 
                   #cont_2<- 0
                   tao<- abs(a_2 * (1+ a_0 +a_1 - a_2 )/((a_0 - a_2)*(a_1 - a_2)))
   
                  S0<-function(a,b){
                     sum<-0
                       i<- 0
                      while(i<=min(a,b)){
                           chis0<-  tao^i *choose(a,i)*choose(b,i)
                           chis1<- choose(v+a+b-1,i)
                           chis2<- chis0 / chis1
                            sum<- sum+ chis2
                              i<- i+ 1
                          }   
                         return(sum)
                      }

                  S1<-function(a,b){
                     sum<-0
                       i<- 0
                      while(i<=min(a,b)){
                               chis0<- i* tao^i *choose(a,i)*choose(b,i)
                               chis1<- choose(v+a+b-1,i)
                               chis2<- chis0 / chis1
                                 sum<- sum+ chis2
                                   i<- i+ 1
                            }   
                         return(sum)
                      }

                  x<- numeric(N)
                  y<- numeric(N)

                 U0<- function(x,y){
                       cont4<- numeric(0)
                       cont4<- 0
                         for(j in 1:N){
                                  g<- S1(x[j],y[j]) / S0(x[j],y[j])
                              cont4<- cont4 + g
                            }
                      res0<- cont4 / N
                      return(res0)
                    }

                
                g_2<- U0(datos_a,datos_b) /v
                if(g_2 < 0  || abs(g_2 - min(a_0 ,a_1))< .4) g_2 <- 0
                return(g_2)                      
   }# fin del metodo de maxima
############################################################################
# DBNB
gmass <- function(gamma0,gamma1,gamma2,N,v){
  if( gamma0 > gamma2 && gamma1> gamma2 && gamma2>=0){  
    p1<- (gamma0- gamma2) /(1+gamma0+gamma1-gamma2)
    p2<- (gamma1- gamma2) /(1+gamma0+gamma1-gamma2)
    p3<- gamma2 /(1+ gamma0 +gamma1 -gamma2 )
    tau <- gamma2 *(1+gamma0 + gamma1- gamma2)/((gamma0- gamma2)*(gamma1- gamma2))
    #print(c(p1,p2,p3))
    x1<- numeric(N)
    x2<- rep(N,0)
     x<- rep(N,0)
     y<- numeric(N)
  chu<- function(a){
      p<- abs(1- (p2 +p3)/(1- p1))
      #print(p)
      ruta1<- choose(v+a-1,v-1)* p^v * (1- p)^a 
      return(ruta1)
    }  
 dy <- unuran.discr.new(pmf=chu , lb=0, ub=10, mode=0, sum=1)
 gen <- unuran.new(distr= dy, method="dari; squeeze=on")
 y<- ur(gen,N)
  chiss<- function(t){
                P<- abs( p3 /(p2 +p3))
                # print(P)
                ruta4<- choose(v,t) *P^t * (1- P)^(v-t)
                return(ruta4)
              }
        dxg <- unuran.discr.new(pmf= chiss, lb=0, ub=2, mode=0, sum=1)
        gen <- unuran.new(distr= dxg, method="dari; squeeze=on")
        x1<-ur(gen,N)
 for(j in 1:N){
         chua<- function(b){
                px2<- abs(1- p1)
                #print(px2)
                ruta3<- choose(v+y[j]+b-1,v+y[j]-1) * px2^(v+y[j]) * (1- px2)^b
                return(ruta3)
             }
       dx2 <- unuran.discr.new(pmf= chua, lb=0, ub=10, mode=0, sum=1)
       gen <- unuran.new(distr= dx2, method="dari; squeeze=on")
      x2[j]<-ur(gen,1)
       x[j]<- x1[j]+x2[j]
    }# fin de for  
         return(list(x=x,y=y))
   }# fin de if
     else 
     { 
       stop("Los parametros no cumplen los requisitos")
       on.exit    
     }  
 }# fin de DBNB
############################################################################
N<- 50
v<- 4
M <- 50
B <- 25
vp05_bn <- vp10_bn <- 0
vp_bn <- rep(0,M)
load("PB.rda")
  for (m in 1:M){     
      datosx<- PB[[m]]$x
      datosy<- PB[[m]]$y
      tablapoiss<- table(datosx,datosy)
      gamma_0<-  mean(datosx)/v
      gamma_1<-  mean(datosy)/v
      gamma_2<-  freczero(a_0=gamma_0,a_1=gamma_1,tabla=tablapoiss,N=N,v=v)
      gamma_2x<- est.maxima(datos_a=datosx,datos_b=datosy,a_0=gamma_0,a_1=gamma_1,a_2=gamma_2,N=N,v=v)
      B_obs<- B_est(a=gamma_0,b=gamma_1,c=gamma_2x,datos_x=datosx,datos_y=datosy,N=N,v=v)
    for (b in 1:B){      
            respa <- gmass(gamma0=gamma_0,gamma1=gamma_1,gamma2=gamma_2,N=N,v=v)
            datosg<- data.frame(x=respa$x,y=respa$y)
            tabla1<-table(datosg$x,datosg$y)
            gammaboot_0<-  mean(datosg$x)/v
            gammaboot_1<-  mean(datosg$y)/v
            gammaboot_2<- freczero(a_0=gammaboot_0,a_1=gammaboot_1,tabla=tabla1,N=N,v=v)
            gammaboot_2x<- est.maxima(datos_a=datosg$x,datos_b=datosg$y,a_0=gammaboot_0,a_1=gammaboot_1,a_2=gammaboot_2,N,v)
            B_boot<- B_est(a=gammaboot_0,b=gammaboot_1,c=gammaboot_2x,datos_x=datosg$x,datos_y=datosg$y,N,v=v)
            #Acumular una aproximacion del valor p para el estadistico
            if(B_boot >= B_obs) vp_bn[m] <- vp_bn[m] + 1
        } # fin de for anidado
     #Calcular el valor p (bootstrap) para el estadistico  
      vp_bn[m] <- vp_bn[m]/B  
    
     #Acumular valor-p <= \alpha (\alpha = 0.05, 0.1) para cada estadistico
     
    if(vp_bn[m] <= .05) vp05_bn <- vp05_bn + 1
    if(vp_bn[m] <= .10) vp10_bn <- vp10_bn + 1

}# fin de for 
#Calcular el valor p para el estadistico  
vp05_bn <- vp05_bn/M
vp10_bn <- vp10_bn/M  
vp05_bn 
vp10_bn 