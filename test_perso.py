
taille_tableau = 10

tableau = []
for i in range(taille_tableau):
    tableau.append([])
    for j in range(taille_tableau):
        tableau[i].append([])

for i in range(taille_tableau):
    for j in range(taille_tableau):
        tableau[i][j].append(i*j)

print(tableau)