library(ggplot2)
library(gridExtra)

####### MTurk Annotation Results ##########
data1<-read.csv(file="annotation.csv",header=T,sep=",")
data1$LenV<-as.numeric(data1$LenV)
data1$Annotation<-factor(data1$Annotation,levels=c("3 Yes", "2 Yes", "1 Yes", "0 Yes"))
data1$Len<-factor(data1$Len,levels=c("Short PP closer","Long PP closer", "Equal length"))
p1<-ggplot(data1,aes(x=Len,y=LenV,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(LenV,"%")), vjust=-1,position=position_dodge(.9),size=2.5)+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="Percent (%)")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,70))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank())+theme(legend.position="top")+
  facet_wrap(~Annotation,ncol=4)
p1

####### Plotting DLM ####
data1<-read.csv(file="dlm-vprep-new.csv",header=T,sep=",")
data1$Mean<-as.numeric(data1$Mean)
data1$Len<-factor(data1$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
data1$Language<-factor(data1$Language,levels=c("Danish", "Norwegian", "Swedish", "Slovak", "Serbian", "Arabic", "Hebrew", "Greek", "Indonesian", "Galician", "Latvian", "Irish"))

p1<-ggplot(data1[,],aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-3.5,position=position_dodge(.9),size=2.6)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="Percent (%)")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank())+theme(legend.position="top")+
  facet_wrap(~Language,ncol=6)
p1

ggsave("dlm-vprep.pdf",p1, width=8, height=4)

data2<-read.csv(file="dlm-mix-vprep-new.csv",header=T,sep=",")
data2$Mean<-as.numeric(data1$Mean)
data2$Len<-factor(data2$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
data2$Language<-factor(data2$Language,levels=c("English", "German", "Dutch", "Bulgarian", "Croatian","Czech",
                                               "Russian","Slovenian","Ukrainian", "Polish"))
p2<-ggplot(data2[,],aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-3.5,position=position_dodge(.9),size=3)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="Percent (%)")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank())+theme(legend.position="top")+
  facet_wrap(~Language,ncol=6)

data3<-read.csv(file="romance-dlm-mix-vprep-new.csv",header=T,sep=",")
data3$Mean<-as.numeric(data3$Mean)
data3$Len<-factor(data3$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
p3<-ggplot(data3[,],aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-3.5,position=position_dodge(.9),size=3)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank())+theme(legend.position="none")+
  facet_wrap(~Language,ncol=6)

p4<-grid.arrange(p2, p3,nrow=2,ncol=1,widths=1:1,heights=2:1)

data2<-read.csv(file="dlm-mix-prepv-new.csv",header=T,sep=",")
data2$Mean<-as.numeric(data1$Mean)
data2$Len<-factor(data2$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
data2$Language<-factor(data2$Language,levels=c("English", "German", "Dutch", "Bulgarian", "Croatian","Czech",
"Russian","Slovenian","Ukrainian", "Polish"))

p2<-ggplot(data2[,],aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-3.5,position=position_dodge(.9),size=3)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="Percent (%)")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank())+theme(legend.position="top")+
  facet_wrap(~Language,ncol=6)


data3<-read.csv(file="romance-dlm-mix-prepv-new.csv",header=T,sep=",")
data3$Mean<-as.numeric(data3$Mean)
data3$Len<-factor(data3$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
p3<-ggplot(data3[,],aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-3.5,position=position_dodge(.9),size=3)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank())+theme(legend.position="none")+
  facet_wrap(~Language,ncol=6)

p4<-grid.arrange(p2,p3,nrow=2,ncol=1,widths=1:1,heights=2:1)


########### everything for Postp + V ############

data1<-read.csv(file="dlm-postpv-new.csv", header = T, sep = ",")
data1$Mean<-as.numeric(data1$Mean)
data1$Len<-factor(data1$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
data1$Language<-factor(data1$Language,levels=c("Japanese", "Hindi", "Urdu"))
p1<-ggplot(data1,aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-4.5,position=position_dodge(.9),size=2.6)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="Percent (%)")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.title.y=element_text(size=8))+ 
  theme(legend.position="top")+
  facet_wrap(~Language,ncol=6)

p1

ggsave("dlm-postpv.pdf",p1, width=5, height=3)


######### Everything for Prep + V ######

data1<-read.csv(file="dlm-prepv-new.csv", header = T, sep = ",")
data1$Mean<-as.numeric(data1$Mean)
data1$Len<-factor(data1$Len,levels=c("Shorter PP closer","Longer PP closer", "Equal length"))
data1$Language<-factor(data1$Language,levels=c("Afrikaans", "Persian", "Chinese"))
p1<-ggplot(data1,aes(x=Len,y=Mean,fill=Len)) + 
  geom_bar(position=position_dodge(),stat='identity',colour='black')+
  geom_text(aes(label=paste(Mean,"%")), vjust=-4.5,position=position_dodge(.9),size=2.6)+
  geom_errorbar(aes(ymin=CI25, ymax=CI975),width=.1,position=position_dodge(.9))+
  scale_fill_manual(values=c("#009E73","#999999", "#E69F00"))+
  labs(x="Corpus")+labs(y="Percent (%)")+labs(fill="PP ordering")+
  scale_y_continuous(limits=c(0,100))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.title.y=element_text(size=8))+ 
  theme(legend.position="top")+
  facet_wrap(~Language,ncol=6)

p1

ggsave("dlm-prepv.pdf",p1, width=5, height=3)

