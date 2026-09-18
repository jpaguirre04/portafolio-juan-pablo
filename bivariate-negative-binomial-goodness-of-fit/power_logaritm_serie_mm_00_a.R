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
# metodo de los momentos
########################################################################################
m11<- function(datos_a,datos_b,a_0,a_1,r,s,zaap,n,v){
          c1<- as.numeric(dimnames(zaap)[[1]])
          c2<- as.numeric(dimnames(zaap)[[2]])
          k1<- k2 <- numeric(0)
           h<-numeric(0)
           h<-0
          k1<-k2<-1
           for(i in c1 ){
              for(j in  c2){
                  h<- h + (i- mean(datos_a))^r *(j- mean(datos_b))^s *zaap[k1,k2]
                  k2<-k2+1
              }
             k1<- k1+1
             k2<- 1
       }
       g_2<-  h/(n*v) - a_0 * a_1
      if(g_2< 0 || abs(g_2 - min(a_0 ,a_1))< .20778899) g_2 <- 0
      return(g_2)
    }
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
# LS
lsb<- function(theta1,theta2,theta3,n){
           y<- numeric(n)
         delta<-  -log(1-theta1 -theta2- theta3)
         flm_y<- function(s){
                     ifelse(s>= 1,((theta2+ theta3)/(1-theta1))^s *(s* delta)^(-1),-log(1-theta1)/delta)
                   }
          d_y <- unuran.discr.new(pmf=flm_y, lb=0, ub=10, mode=0, sum=1)
          ## Crear UNU.RAN.
          gen <- unuran.new(distr=d_y, method="dari; squeeze=on")
             y<-ur(gen,n)

          x1<- rep(n,0)
          x2<- rep(n,0)
           x<- rep(n,0)
            for(j in 1:n){
                 if(y[j]>0){  
                               P<-  theta3 / (theta2 +theta3)
                            x1<- rbinom(1,y[j],P) 
                           px2<- abs(1- theta1)
                            x2<- rnbinom(1,y[j],px2)
                              x[j]<- x1 + x2
                             #x[j]<- rbinom(y[j],1,theta3 /(theta2+ theta3))+ rnbinom(y[j],1,1-theta1)
                           }
                      else{
                           fun_0<- function(s){ theta1^s /(-s*log(1-theta1))}
                            d_a <- unuran.discr.new(pmf=fun_0, lb=1, ub=10, mode=0, sum=1)
                           ## Crear UNU.RAN.
                           gen <- unuran.new(distr=d_a, method="dari; squeeze=on")
                           x[j]<-ur(gen,1)
                         }
                  }
          return(list(x=x,y=y))
}
################################################################
# parametros LS
theta1<- .005
theta2<- .005
theta3<- .23
N<- 50
v<- 1
M <- 100
B <- 50
vp05_bn <- vp10_bn <- 0
vp_bn <- rep(0,M)
SLBa= list(0)
  for (m in 1:M){     
      respls<- lsb(theta1=theta1,theta2=theta2,theta3=theta3,n=N)
      datosfls<- data.frame(x=respls$x,y=respls$y)
      muestrals<-data.frame(x=respls$x,y=respls$y)
      SLBa[[m]]<- muestrals
      tablals<-table(datosfls$x,datosfls$y)
      gamma_0<-  mean(datosfls$x)/v
      gamma_1<-  mean(datosfls$y)/v
      gamma_2<-  m11(datosfls$x,datosfls$y,a_0=gamma_0,a_1=gamma_1,r=1,s=1,zaap=tablals,N,v=v)
      B_obs<- B_est(a=gamma_0,b=gamma_1,c=gamma_2,datos_x=datosfls$x,datos_y=datosfls$y,N,v=v)
    for (b in 1:B){      
            respa <- gmass(gamma0=gamma_0,gamma1=gamma_1,gamma2=gamma_2,N=N,v=v)
            datosg<- data.frame(x=respa$x,y=respa$y)
            tabla1<-table(datosg$x,datosg$y)
            gammaboot_0<-  mean(datosg$x)/v
            gammaboot_1<-  mean(datosg$y)/v
            gammaboot_2<- m11(datosg$x,datosg$y,a_0=gammaboot_0,a_1=gammaboot_1,r=1,s=1,zaap=tabla1,N,v=v)
            B_boot<- B_est(a=gammaboot_0,b=gammaboot_1,c=gammaboot_2,datos_x=datosg$x,datos_y=datosg$y,N,v=v)
            #Acumular una aproximacion del valor p para el estadistico
            if(B_boot >= B_obs) vp_bn[m] <- vp_bn[m] + 1
        } # fin de for anidado
     #Calcular el valor p (bootstrap) para el estadistico  
      vp_bn[m] <- vp_bn[m]/B  
    
     #Acumular valor-p <= \alpha (\alpha = 0.05, 0.1) para cada estadistico
     
    if(vp_bn[m] <= .05) vp05_bn <- vp05_bn + 1
    if(vp_bn[m] <= .10) vp10_bn <- vp10_bn + 1

}# fin de for
save(SLBa, file="SLBa.rda") 
#Calcular el valor p para el estadistico  
vp05_bn <- vp05_bn/M
vp10_bn <- vp10_bn/M  
vp05_bn 
vp10_bn 