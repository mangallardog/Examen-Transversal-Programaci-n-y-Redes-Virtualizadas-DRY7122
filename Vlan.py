n_vlan=int(input("Ingrese el número de Vlan: "))
if n_vlan>=1 and n_vlan<=1005:
	print("La Vlan ", n_vlan, " corresponde al rango normal.")
elif n_vlan>=1006 and n_vlan<=4094:
	print("La Vlan ", n_vlan, " corresponde al rango extendido")

