dat = read.csv('Results.csv')

plot(y=dat$Baseline, x=dat$NumRecs, ylim=c(min(dat$Baseline),max(dat$Baseline)), 
	xlim=(c(1,10)), col="red", pch=19, xaxt="n")
pos = c(1,3,5,10)
axis(1, at=pos, labels=pos)
lines(y=dat$Baseline, x=dat$NumRecs, col="red")

points(y=dat$UserBased10, x=dat$NumRecs, col="purple", pch=19)
lines(y=dat$UserBased10, x=dat$NumRecs, col="purple")

points(y=dat$UserBased20, x=dat$NumRecs, col="green", pch=19)
lines(y=dat$UserBased20, x=dat$NumRecs, col="green")

points(y=dat$ItemBased, x=dat$NumRecs, col="blue", pch=19)
lines(y=dat$ItemBased, x=dat$NumRecs, col="blue")