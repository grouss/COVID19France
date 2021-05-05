def convertstring2date(date):
    # try AAAA-MM-JJ
    d=date.replace('\"','')
    if '-' in d:
        d=d.split('-')
        for i in range(len(d)):
            d[i]=int(d[i])
        if (d[0]==2020 or d[0]==2021) and (d[1]<13 and d[1]>0) and (d[2]>0 and d[2]<32):
            return d[0],d[1],d[2]
    print(d)
    return "Error"

def ReadClasseAge(dx):
    flist=[]
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, "donnees-hospitalieres-classe-age-covid19-"+dx+"*.csv"):
            flist.append(path+file)
        
    if len(flist)!=1:
        print("Error plus d'un fichier")
    else:
        filename=flist[0]
        print("Read ",filename)
        #region
        #print(" open",path+file)
        f=open(filename,"r")
        c=f.readlines()
        #print(0,c[0].rsplit(';'))
        #print(1,c[1].rsplit(';'))
        # pour éviter les problèmes lors des permutations de colonnes dans les données
        fields={}
        cc=c[0].replace('\"','').replace('\n','').rsplit(';')
        for i in  range(len(c[0].rsplit(';'))):
            if  cc[i]=='reg':fields["reg"]=i
            if  cc[i]=='cl_age90':fields["clage"]=i
            if  cc[i]=='jour':fields["jour"]=i
            if  cc[i]=='hosp':fields["hosp"]=i
            if  cc[i]=='rea':fields["rea"]=i
            if  cc[i]=='dc':fields["dc"]=i
            if  cc[i]=='rad':fields["rad"]=i
        data3={}
        i=0
        for j in range(1,len(c)):
            cc=c[j].replace('\"','').replace('\n','').rsplit(';')
            dat=cc[fields["jour"]]
            reg=cc[fields["reg"]]
            if reg!='NA' and int(reg)>=11:
                # on exclue temporairement reg=01, 02, 03, 04 , 02 car le fichier est
                # est corrompu à partie du 12/11/2020 (manque une tranche d'age)
                clage=int(cc[fields["clage"]].replace('\"',''))
                hosp=int(cc[fields["hosp"]])
                rea=int(cc[fields["rea"]])
                # ! format different pour fichier hospi classe age
                rad=int(cc[fields["rad"]])
                dc=int(cc[fields["dc"]])
                AAAA,MM,JJ=convertstring2date(dat)
                if reg not in data3: data3[reg]={}
                if clage not in data3[reg]: data3[reg][clage]=[]
                data3[reg][clage].append([dt(AAAA,MM,JJ),hosp,rea,dc,rad])

        fields=["hosp","rea","dc","rad"]
        dfields=3 # 3 or 4

        for reg in data3:
            for clage in data3[reg]:
                try:
                    data3[reg][clage]=np.array(data3[reg][clage])
                except:
                    print("Erreur",reg,clage)
    return data3,fields,dfields


def ReadNouveaux(dx):
    flist=[]
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, "donnees-hospitalieres-nouveaux-covid19-"+dx+"*.csv"):
            flist.append(path+file)
        
    if len(flist)!=1:
        print("Error plus d'un fichier ou aucun")
    else:
        filename=flist[0]
        print("Read ",filename)
        f=open(filename,"r")
        #file="donnees-hospitalieres-nouveaux-covid19-"+dx+"-19h00.csv"
        #print("open ",file)
        #f=open(file,"r")
        c=f.readlines()
        #print(0,c[0].rsplit(';'))
        #print(1,c[1].rsplit(';'))
        dataN={}
        for i in range(1,len(c)):
        #    l=c[i].rsplit(',')
            l=c[i].replace('\"','').replace('\n','').rsplit(';')
            dep=l[0]
            hospi=int(l[2])
            rea=int(l[3])
            dc=int(l[4])
            rad=int(l[5])
            a=int(l[1][:4])
            m=int(l[1][5:7])
            j=int(l[1][8:10])
            #print(l[1],a,m,j,dt(a,m,j))
            if i!=0:
                if dep not in dataN: dataN[dep]=[]
                try:
                    #dataN[dep][dt(a,m,j)]=[hospi,rea,dc]
                    dataN[dep].append([dt(a,m,j),hospi,rea,dc,rad])
                except:
                    print("Error1",dep,a,m,j,hospi,rea,dc,rad)
                #print(date,a,m,j)
        for reg in dataN:
            try:
                dataN[reg]=np.array(dataN[reg])
            except:
                print("Erreur",reg)
    return dataN
            
            
def AddRectangles(axs,ymax,ymin):
    someX,someY=debut_confinement_1,ymin
    dx,dy=fin_confinement_1-debut_confinement_1,ymax-ymin
    axs.add_patch(Rectangle((someX, someY), dx, dy, color = '#9467bd', alpha=0.35))

    someX,someY=debut_couvrefeu_1,ymin
    dx,dy=fin_couvrefeu_1-debut_couvrefeu_1,ymax-ymin
    axs.add_patch(Rectangle((someX, someY), dx, dy, color = '#e377c2', alpha=0.10))

    someX,someY=debut_confinement_2,ymin
    dx,dy=fin_confinement_2-debut_confinement_2,ymax-ymin
    axs.add_patch(Rectangle((someX, someY), dx, dy, color = '#9467bd', alpha=0.35))

    someX,someY=debut_couvrefeu_2,ymin
    dx,dy=fin_couvrefeu_2-debut_couvrefeu_2,ymax-ymin
    axs.add_patch(Rectangle((someX, someY), dx, dy, color = '#e377c2', alpha=0.10))
    
    someX,someY=debut_confinement_3,ymin
    dx,dy=fin_confinement_3-debut_confinement_3,ymax-ymin
    axs.add_patch(Rectangle((someX, someY), dx, dy, color = '#9467bd', alpha=0.20))
    
    someX,someY=debut_confinement_4,ymin
    dx,dy=fin_confinement_4-debut_confinement_4,ymax-ymin
    axs.add_patch(Rectangle((someX, someY), dx, dy, color = '#9467bd', alpha=0.35))
    
def DisplayAge(clage,normed=False):
    if clage in trancheage:
        print()
        print(trancheage[clage])
        #fig, axs = plt.subplots(1, 4,figsize=(20,5))
        fig, axs = plt.subplots(1, dfields,figsize=(20,5))
        xx=data3["11"][clage][:,0]
        yy=np.zeros((len(xx),4))            
        for reg in data3:
            yy+=data3[reg][clage][:,1:5]
        if normed==True and clage!=0:
            yy0=np.zeros((len(xx),4))
            for reg in data3:
                yy0+=data3[reg][0][:,1:5]
            yy=yy/yy0
        for i in range(2):
            if normed==True and clage!=0:
                axs[i].set_ylim([1e-4,1])
                axs[i].set_title(fields[i]+" en France")
                print(f' Max   {fields[i]:4} : {int(np.max(yy[:,i])):5} | 1ère Vague :{int(np.max(yy[:,i][xx<7])):5} | 2ème Vague :{int(np.max(yy[:,i][xx>7])):5} |')
                AddRectangles(axs[i],1,1e-4)
                axs[i].semilogy(xx,yy[:,i],label=trancheage[clage],color=color[i])

            else:
                ymin=np.min(yy[:,i])
                ymax=np.max(yy[:,i])
                if ymin>0: 
                    ymin=int(np.log10(ymin))
                else:
                    ymin=-1
                if ymax>0: 
                    ymax=int(np.log10(ymax))+1
                else:
                    ymax=ymin+1
                if ymax==ymin:
                    ymax=ymin+1
                axs[i].set_ylim([10**ymin,10**ymax])
                axs[i].set_title(fields[i]+" en France")
                print(f' Max   {fields[i]:4} : {int(np.max(yy[:,i])):5} | 1ère Vague :{int(np.max(yy[:,i][xx<7])):5} | 2ème Vague :{int(np.max(yy[:,i][xx>7])):5} |')
                AddRectangles(axs[i],10**ymax,10**ymin)
                axs[i].semilogy(xx,yy[:,i],label=trancheage[clage],color=color[i])


        n=7
        #for i in range(2,4):
        for i in range(2,dfields):

            Delta=(xx[n:]-xx[0:-n])/(dt(2020,1,2)-dt(2020,1,1))
            zz=(yy[n:,i]-yy[0:-n,i])/Delta
            #if min(zz)<0:
            #  print(clage,i,min(zz),xx[n:][zz<0],zz[zz<0])
            zmin=np.min(zz)
            zmax=np.max(zz)
            if zmin>0: 
                zmin=int(np.log10(zmin))
            else:
                zmin=-1
            if zmax>0: 
                zmax=int(np.log10(zmax))+1
            else:
                zmax=zmin+1
            if zmax==zmin:
                zmax=zmin+1
            if normed==True and clage!=0:
                axs[i].set_ylim([1e-4,1])
                axs[i].set_title(fields[i]+" en France (moyenne hedbo)")
                print(f' Max   {fields[i]:4} : {int(np.max(zz)):5} | 1ère Vague :{int(np.max(zz[xx[n:]<7])):5} | 2ème Vague :{int(np.max(zz[xx[n:]>7])):5} |')
                AddRectangles(axs[i],1,1e-4)
                axs[i].semilogy(xx,yy[:,i],label=trancheage[clage],color=color[i])
            else:
                axs[i].set_ylim([10**zmin,10**zmax])
                axs[i].set_title(fields[i]+" en France (moyenne hedbo)")
                print(f' Max   {fields[i]:4} : {int(np.max(zz)):5} | 1ère Vague :{int(np.max(zz[xx[n:]<7])):5} | 2ème Vague :{int(np.max(zz[xx[n:]>7])):5} |')
                print(f' Total {fields[i]:4} : {int(np.sum(zz)):5} | 1ère Vague: {int(np.sum(zz[xx[n:]<7])):5} | 2ème Vague :{int(np.sum(zz[xx[n:]>7])):5} |')
                AddRectangles(axs[i],10**zmax,10**zmin)
                axs[i].semilogy(xx[n:][zz>0],zz[zz>0],"o",markersize=2,label=trancheage[clage]+" par jours",color=color[i])

        #for i in range(4):
        for i in range(dfields):
            axs[i].set_xticks(list(range(1,19)))
            axs[i].set_xticklabels([
                "Jan\n20","Fev\n20","Mar\n20",
                "Avr\n20","Mai\n20","Jun\n20",
                "Jul\n20","Aou\n20","Sep\n20",
                "Oct\n20","Nov\n20","Dec\n20",
                "Jan\n21","Fev\n21","Mar\n21",
                "Avr\n21","Mai\n21","juin\n21"
            ],ha="left")
            axs[i].legend()
            axs[i].grid(which="both")
            axs[i].set_xlim(2.99,18.99)

        plt.show()
def AddRectangleFrance(currentAxis,ymax=1e5,ymin=1):
    someX,someY=debut_confinement_1,ymin
    dx,dy=fin_confinement_1-debut_confinement_1,ymax-ymin
    currentAxis.add_patch(Rectangle((someX, someY), dx, dy, color = "c", alpha=0.35))

    someX,someY=debut_couvrefeu_1,ymin
    dx,dy=fin_couvrefeu_1-debut_couvrefeu_1,ymax-ymin
    currentAxis.add_patch(Rectangle((someX, someY), dx, dy, color = "c", alpha=0.10))

    someX,someY=debut_confinement_2,ymin
    dx,dy=fin_confinement_2-debut_confinement_2,ymax-ymin
    currentAxis.add_patch(Rectangle((someX, someY), dx, dy, color = "c", alpha=0.35))

    someX,someY=debut_couvrefeu_2,ymin
    dx,dy=fin_couvrefeu_2-debut_couvrefeu_2,ymax-ymin
    currentAxis.add_patch(Rectangle((someX, someY), dx, dy, color = "c", alpha=0.10))

    someX,someY=debut_confinement_3,ymin
    dx,dy=fin_confinement_3-debut_confinement_3,ymax-ymin
    currentAxis.add_patch(Rectangle((someX, someY), dx, dy, color = "c", alpha=0.20))

    someX,someY=debut_confinement_4,ymin
    dx,dy=fin_confinement_4-debut_confinement_4,ymax-ymin
    currentAxis.add_patch(Rectangle((someX, someY), dx, dy, color = "c", alpha=0.35))
    

def DisplayFrance(xmin=3,xmax=18,ymin=1,ymax=1e5):
    plt.figure(figsize=(20,5))
    # 
    currentAxis = plt.gca()
    AddRectangleFrance(currentAxis,1e5,1)
    
    for clage in [0]:
        xx=data3["11"][clage][:,0]
        yy=np.zeros((len(xx),4))
        for reg in data3:
            yy+=data3[reg][clage][:,1:5]
    stitle=""
    for i in range(2):
        plt.semilogy(xx,yy[:,i],label=fields[i]+" en France")
        stitle+=fields[i]+" (en France) : "+str(int(yy[-1,i]))
        stitle+=" ("+str(int(yy[-1,i]-yy[-2,i]))+")"
        stitle+=" max "+str(int(max(yy[:,i])))+" | "
        #print(fields[i], ((yy[n:,i]))[-1]," max ",np.max(yy[n:,i]))
    n=7
    for i in range(2,dfields):   
        Delta=(xx[n:]-xx[0:-n])/(dt(2020,1,2)-dt(2020,1,1))
        zz=(yy[n:,i]-yy[0:-n,i])/Delta
        plt.semilogy(xx[n:],zz,label=fields[i]+" par jours (moy hebdo)")
        stitle+=fields[i]+" (par jours) : "+str(int(zz[-1]))
        stitle+=" ("+str(int(zz[-1]-zz[-2]))+")"
        stitle+=" max "+str(int(max(zz[:])))

    # affichage de la période du premier confinement

    plt.legend(loc='lower left')
    plt.grid(which='both')
    plt.title(stitle)
    plt.xticks(list(range(1,19)),["Janvier\n2020","Février\n2020","Mars\n2020",
                                  "Avril\n2020","Mai\n2020","Juin\n2020",
                                  "Jully\n2020","Aout\n2020","Septembre\n2020",
                                  "Octobre\n2020","Novembre\n2020","Décembre\n2020",
                                  "Janvier\n2021","Février\n2021","Mars\n2021",
                                  "Avril\n2021","Mai\n2021","Juin\n2021"
                                 ],ha="left")
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.show()
    # flux +/- Rea
    # flux  +/- Hospi
    xx=dataN["11"][:,0]
    for reg in dataN[reg]:
        zz=np.zeros((len(xx),4))
        for reg in dataN:
            zz+=dataN[reg][:,1:5]
    #print(yy[0,:])
    n=7
    for i in range(2):
        plt.figure(figsize=(20,5))
        currentAxis = plt.gca()
        if i==0:
            AddRectangleFrance(currentAxis,1e4,10)
            plt.ylim(10,1e4)
        else:
            AddRectangleFrance(currentAxis,1e3,5)
            plt.ylim(5,1e3)

            
        vv=np.cumsum(zz[:,i])
        #plt.semilogy(xx,np.cumsum(yy[:,i]),label=fields[i]+" en France XX")
        Delta=(xx[n:]-xx[0:-n])/(dt(2020,1,2)-dt(2020,1,1))
        #plt.semilogy(xx[n:],(yy[n:,i]-yy[0:-n,i])/Delta,label=fields[i]+" par jours (moy hebdo)")
        soldeplus=(vv[n:]-vv[0:-n])/Delta
        solde=(yy[1+n:,i]-yy[1:-n,i])/Delta
        soldemoins=solde-soldeplus
        plt.semilogy(xx[n:],soldeplus,label="Entrées",color="red")
        #print(len(xx[n:]),len(vv[n:]),len(vv[0:-n]),len(yy[n:,i]),len(yy[0:-n,i]))
        # on exclue la première valeur qui n'est pas commune entre le deux jeux de données
        plt.semilogy(xx[n:],abs(soldemoins),label="Sorties",color="green")
        plt.legend(loc='lower left')
        plt.grid(which='both')
        plt.title("Flux "+fields[i]+" par jours (moy hebdo) en France "
                  +str(int(soldeplus[-1]-abs(soldemoins[-1])))
                  +"=("+str(int(soldeplus[-1]))+str(int(soldemoins[-1]))+")")
        plt.xticks(list(range(1,19)),["Janvier\n2020","Février\n2020","Mars\n2020",
                                  "Avril\n2020","Mai\n2020","Juin\n2020",
                                  "Jully\n2020","Aout\n2020","Septembre\n2020",
                                  "Octobre\n2020","Novembre\n2020","Décembre\n2020",
                                  "Janvier\n2021","Février\n2021","Mars\n2021",
                                "Avril\n2021","Mai\n2021","Juin\n2021"
                                 ],ha="left")
        plt.xlim(xmin,xmax)
        plt.show()

def DisplayRegions(reg):
    if reg in data3:
        
        print()
        print(region[reg]+" ("+trancheage[0]+")")
        #fig, axs = plt.subplots(1, 4,figsize=(20,5))
        fig, axs = plt.subplots(1, dfields,figsize=(20,5))
        for i in range(dfields):
            axs[i].set_xticks(list(range(1,19)))
            axs[i].set_xticklabels([
                "Jan\n20","Fev\n20","Mar\n20",
                "Avr\n20","Mai\n20","Jun\n20",
                "Jul\n20","Aou\n20","Sep\n20",
                "Oct\n20","Nov\n20","Dec\n20",
                "Jan\n21","Fev\n21","Mar\n21",
                "Avr\n21","Mai\n21","Juin\n21"
            ],ha="left")
            axs[i].set_xlim(2.99,18.99)

        #for clage in data3[reg]:
        for clage in [0]:
            #print(axs)
            for i in range(2):
                x=data3[reg][clage][:,0]
                y=data3[reg][clage][:,i+1]
                AddRectangles(axs[i],1.2*max(y),0*min(y))
                axs[i].set_ylim(0*min(y),max(y)*1.2)
                axs[i].plot(x,y,label=trancheage[clage],color=color[i])
                axs[i].set_title(fields[i])
                axs[i].grid(which="both")
              
            n=7
            for i in range(2,dfields):              
                x=data3[reg][clage][:,0]
                Delta=(x[n:]-x[0:-n])/(dt(2020,1,2)-dt(2020,1,1))
                y=(data3[reg][clage][n:,i+1]-data3[reg][clage][0:-n,i+1])/Delta
                AddRectangles(axs[i],1.2*max(y),0*min(y))
                axs[i].set_ylim(0*min(y),max(y)*1.2)
                axs[i].plot(x[n:],y,"o",markersize=2,label=trancheage[clage],color=color[i])
                axs[i].set_title(fields[i]+ " par jours (moy hebdo)")
                axs[i].grid(which="both")
        plt.show()


def UpdateData(Verbose=False):
    dx="0000-00-00"
    s=os.popen('wget -m -k -p -np  https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/')
    #print(s.read())
    time.sleep(5)
    f=open("www.data.gouv.fr//fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/index.html","r")
    L=(f.read()).split('\"')
    #print(len(L))
    for  l in L:
        if l[-3:]=="csv" and l[:5]=="https":
            d=l.split('/')
            if d[-1][:7]=="donnees":
                os.system('wget '+l+' -O RawData/'+d[-1])
                if Verbose: print(d[-1],d[-1][-20:-10],dx)
                if dx<d[-1][-20:-10]: dx=d[-1][-20:-10]
    PushCommit("Data Update")    
    return dx
def CreateReport(Filename="COVID19_France_Regions"):
    os.system('jupyter nbconvert --to latex '+Filename+'.ipynb')
    os.system('pdflatex '+Filename+'.tex')
    os.system('pdflatex '+Filename+'.tex')
    
def PushCommit(Message=None):
    if Message==None: Message="Mise à jour du rapport "+str(datetime.now())[:10]
    os.system('jupyter nbconvert --to Markdown README.ipynb')
    Filename="COVID19_France_Regions"
    time.sleep(32) # autosave has been set to 30s
    os.system('git add '+Filename+'.pdf')
    os.system('git add ./RawData/*csv')
    os.system('git add ./README.md')
    os.system('git add '+Filename+'.ipynb')
    os.system('git add load.py')
    #os.system('git add Rapports/COVID19_France_Regions.pdf')
    os.system('git add function.py')
    os.system('git commit -m "'+Message+'"')
    os.system('git push')
    
#Verbose=True
#dx=UpdateData()
#print(dx)