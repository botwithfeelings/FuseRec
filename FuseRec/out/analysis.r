dat = read.csv('Results.csv')

dev.new()
setEPS()

postscript("graph.eps")

plot(y=dat$Baseline, x=dat$NumRecs,	xlim=c(1,4), ylim=c(0,1), col="red", pch=19, yaxt="n", xaxt="n", ylab="Success Rate", 
	xlab="Number of Recommendations", main="Success Rate by Number of Recommendations")

pos = c(1,2,3,4)
vals = c(1,3,5,10)

axis(1, at=pos, labels=vals)

pos2 = c(0.2, 0.4, 0.6, 0.8)
vals = c("20%", "40%", "60%", "80%")

axis(2, at=pos2, labels=vals)

abline(h=pos2,v=pos, col="gray",lty=3)

lines(y=dat$Baseline, x=dat$NumRecs, col="red")

points(y=dat$UserBased10, x=dat$NumRecs, col="darkorchid4", pch=19)
lines(y=dat$UserBased10, x=dat$NumRecs, col="darkorchid4")

points(y=dat$UserBased20, x=dat$NumRecs, col="darkgreen", pch=19)
lines(y=dat$UserBased20, x=dat$NumRecs, col="darkgreen")

points(y=dat$ItemBased, x=dat$NumRecs, col="blue", pch=19)
lines(y=dat$ItemBased, x=dat$NumRecs, col="blue")

legend("bottomright", "Algorithm", bg="white", c("User Based 10", "User Based 20", "Baseline", "Item Based"), 
	inset=.03, fill=c("darkorchid4","darkgreen","red","blue"))

dev.off()

graphics.off()