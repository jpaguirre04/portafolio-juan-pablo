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
                 S[i,j]<- 1/((datos_x[i]+datos_x[j]+1+1)*(datos_y[i]+datos_y[j]+1))
             }
          }
       B<- sum(S)/N
       i<- j <- 1:N
       k<- l <- m <- 0:(N-1)
       g<- function(k,l,m,p1,p2,p3,q,v,N){choose(k,l)*choose(k-l,m)* p1^(k-l-m) * p2^l *p3^m *(q^v *N*choose(2*v+k-1,k)*(1/((k-l+1+1)*(l+m+1)))-2* choose(v+k-1,k) *1/((datos_x[i]+k-l+1)*(datos_y[i]+l+m+1)))}
       J<- q^v * sum(outer(k,l,m,p1,p2,p3,q,v,N,FUN=g),na.rm=TRUE)
       TOT<- B+J
       return(TOT)                      
 }# fin de B_est
########################################################################################    
# metodo de los momentos
########################################################################################
m11<- function(datos_a,datos_b,a_0,a_1,a_2,r,s,zaap,n,v){
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
########################################################################################################### 


gmass <- function(gamma0,gamma1,gamma2,N,v){
  if( gamma0 > gamma2 && gamma1> gamma2 && gamma2>=0){  
    p1<- (gamma0- gamma2) /(1+gamma0+gamma1-gamma2)
    p2<- (gamma1- gamma2) /(1+gamma0+gamma1-gamma2)
    p3<- gamma2 /(1+ gamma0 +gamma1 - gamma2)
    tau <- gamma2 *(1+gamma0 + gamma1- gamma2)/((gamma0- gamma2)*(gamma1- gamma2))
    #print(c(p1,p2,p3))
    x1<- rep(N,0)
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
    
 for(j in 1:N){
          chiss<- function(t){
                P<- abs( p3 /(p2 +p3))
                # print(P)
                ruta4<- choose(y[j],t) *P^t * (1- P)^(y[j]-t)
                return(ruta4)
              }
        dxg <- unuran.discr.new(pmf= chiss, lb=0, ub=1, mode=0, sum=1)
        gen <- unuran.new(distr= dxg, method="dari; squeeze=on")
        x1[j]<-ur(gen,1) 
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
}
############################################################################
gamma0<- .35
gamma1<- .35
gamma2<- .007375
v<- 7
N<- 30
M<- 100
C<- 50
vp_B<- numeric(M)
# B_obs<- numeric(M)
B_boot<- numeric(C)
Rucaa= list(0)
for(k in 1:M){
    resp <- gmass(gamma0,gamma1,gamma2,N,v)
    datosf<- data.frame(x=resp$x,y=resp$y)
    muestra<-data.frame(x=resp$x,y=resp$y)
    Rucaa[[k]]<- muestra
    tabla<-table(datosf$x,datosf$y)
    gamma_0<-  mean(datosf$x)/v
    gamma_1<-  mean(datosf$y)/v
    gamma_2<-  m11(datosf$x,datosf$y,a_0=gamma_0,a_1=gamma_1,a_2=gamma2,r=1,s=1,zaap=tabla,N,v)
     g <- 1+gamma_0+gamma_1-gamma_2
     p1 <- (gamma_0-gamma_2)/g
     p2 <- (gamma_1-gamma_2)/g
     p3 <- gamma_2/g
     EX <- (p1+p3)*v*g
     EY <- (p2+p3)*v*g
     VX <- EX*((p1+p3)*g+1)
     VY <- EY*((p2+p3)*g+1)
     ro <- (p3+p1*p2)/sqrt((1-p1)*(1-p2)*(p1+p3)*(p2+p3))
     if(ro>0 && abs(VX/EX-1)<1 && abs(VY/EY-1)<1)
     {
        B_obs<- B_est(a=gamma_0,b=gamma_1,c=gamma_2,datos_x=datosf$x,datos_y=datosf$y,N,v)}
        else{
               stop("Los parametros no cumplen los requisitos")
               on.exit
          }
    #print(B_obs)
                 for(j in 1:C){
                               respa <- gmass(gamma_0,gamma_1,gamma2=gamma_2,N,v)
                               datosg<- data.frame(x=respa$x,y=respa$y)
                               tabla1<-table(datosg$x,datosg$y)
                          gammaboot_0<-  mean(datosg$x)/v
                          gammaboot_1<-  mean(datosg$y)/v
                          gammaboot_2<- m11(datosg$x,datosg$y,a_0=gammaboot_0,a_1=gammaboot_1,a_2=gamma2,r=1,s=1,zaap=tabla1,N,v)
                             B_boot[j]<- B_est(a=gammaboot_0,b=gammaboot_1,c=gammaboot_2,datos_x=datosg$x,datos_y=datosg$y,N,v)
                     }# fin de for anidado
       #print(B_boot)
       vp_B[k]=sum(rep(1,C)[B_boot > B_obs])/C
   }# fin de for principal
#print(vp_B)
save(Rucaa, file="Rucaa.rda")  
B05=sum(rep(1,M)[vp_B<=0.05])/M
B10=sum(rep(1,M)[vp_B<=0.10])/M
B05
B10