import os
#os.system("vmd -dispdev text -e extract.tcl P2.pdb")
#os.system("vmd -dispdev text -e extract.tcl " + str(os.getcwd().split("/")[-1]) + ".pdb")

def tipo(LL):
	c = 0
	while c < 1:
		try:
			c += int(LL)
			return int(LL)+1
		except:
			LL = raw_input("nop: ")
xc = []
yc = []
zc = []

xc.append(tipo(raw_input("ingresa coordenada x minima: ")))
xc.append(tipo(raw_input("ingresa coordenada x maxima: ")))
yc.append(tipo(raw_input("ingresa coordenada y minima: ")))
yc.append(tipo(raw_input("ingresa coordenada y maxima: ")))
zc.append(tipo(raw_input("ingresa coordenada z minima: ")))
zc.append(tipo(raw_input("ingresa coordenada z maxima: ")))


receptor = raw_input("input pdbqt receptor")
ligando = raw_input("input pdbqt ligand")
spacing = 0.375
p = 8 #Numero de procesadores
shift_x = 7.55
shift_y = 8.65
shift_z = 10.5

x = []
x_i = xc[0] + shift_x
for i in range(10):
	x.append(x_i)
	x_i += shift_x

y = []
y_i = yc[0] + shift_y
for i in range(10):
	y.append(y_i)
	y_i += shift_y

z = []
z_i = zc[0] + shift_z
for i in range(10):
	z.append(z_i)
	z_i += shift_z

coordenadas = []
for i in x:
	for f in y:
		for g in z:
			ch = str(i) + "," + str(f) + "," + str(g)
			coordenadas.append(ch)

carpetas = []
for i in range(1,p+1):
	carpetas.append(str(i))
for i in carpetas:
	os.system("rm -r " + i + "/")
	os.system("mkdir " + i)

os.system("rm -r gpf/")
os.system("mkdir gpf/")

os.system("rm -r glg/")
os.system("mkdir glg/")

os.system("rm -r dlg/")
os.system("mkdir dlg/")

gpf = []
glg = []
dlg = []
dpf = ligando + ".dpf"


os.system("./prepare_dpf42.py -r " + str(receptor) + " -l " + ligando + ".pdbqt -o " + dpf)


#copias dpf a todas las carpetas ANIADIR
for i in carpetas:
	os.system("cp " + dpf + " " + i)
	os.system("cp " + receptor + " " + i)
	os.system("cp "+ligando+".pdbqt " + i)

a = str()
for i in range (1,len(coordenadas)+1):
	a = "gpf" + str(i) + ".gpf"
	gpf.append(a)
	a = "glg" + str(i) + ".glg"
	glg.append(a)
	a = ligando + str(i) + ".dlg"
	dlg.append(a)

t=1
gpf_prep = str()
for i in coordenadas:
	gpf_prep = gpf_prep + "./prepare_gpf4.py -r "+ receptor + " -o gpf/gpf" + str(t) + ".gpf -p ligand_types='A,C,NA,OA,HD,N' -p gridcenter='" + str(i) + "' -p spacing='" + str(spacing) + "' -p npts='41,23,56'" + '\n'
	t = t + 1
outfile = open("gpf_prep.sh","w")
outfile.write(gpf_prep)
outfile.close()


os.system("sh gpf_prep.sh")
os.system("mv gpf_prep.sh gpf/")
	
m = int(len(coordenadas) / p)
yyy = len(coordenadas) % p
n = 1
for i in carpetas:
	k = "cd " + str(i) + "/" + '\n'	
	for e in range (0,m):
		k = k + "autogrid4 -p ../gpf/gpf" + str(n) + ".gpf -l ../glg/glg" + str(n) + ".glg " + '\n' + "autodock4 -p poa.dpf -l ../dlg/poa" + str(n) + ".dlg" + '\n'
		n = n + 1
	f = "run" + str(i) + ".sh"
	outfile = open(f,"w")
	outfile.write(k)
	outfile.close()
if yyy != 0 and yyy != 1:
	for j in range(1,yyy+1):
		pp = ""
		k = "autogrid4 -p ../gpf/gpf" + str(n) + ".gpf -l ../glg/glg" + str(n) + ".glg " + '\n' + "autodock4 -p poa.dpf -l ../dlg/poa" + str(n) + ".dlg" '\n'
		n = n + 1
		infile = open("run" + str(j) + ".sh","r")

		for line in infile:
			pp = pp + line
		infile.close()
		pp = pp + k
		outfile = open("run" + str(j) + ".sh","w")
		outfile.write(pp)
		outfile.close()
elif yyy == 1:
	pp = ""	
	infile = open("run1.sh","r")
	for line in infile:
		pp = pp + line
	infile.close()
	outfile = open("run1.sh","w")
	pp = pp + "autogrid4 -p ../gpf/gpf" + str(n) + ".gpf -l ../glg/glg" + str(n) + ".glg " + '\n' + "autodock4 -p poa.dpf -l ../dlg/poa" + str(n) + ".dlg" + '\n'
	outfile.write(pp)
	outfile.close()	

outfile = open("run.sh", "w")
o = ""
for i in range(1,8):
	o = o + "sh run" + str(i) + ".sh | "
o = o + "sh run8.sh"
outfile.write(o)
outfile.close()
os.system("sh run.sh")


...
