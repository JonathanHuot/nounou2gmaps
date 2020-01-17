Convertion to txt works well, but not with ugly pdf like nounous.
To have a complete working TXT, copy/paste the PDF context by selecting the text (manually)
paste into a document, then add new lines based on regex. Note that all the fields are working too!
Nightmare.

Suggestions:

grément\(.*\)$ → 
\1
(then remove the header lines manually)

([^0-9]+)$ → 
\1( Madame )
\(202[0-9]\)\(.*\)$ → \1
\2
Périsco → 
Périsco
Journ → 
Journ
13600 → 
13600
LA CIOTAT → LA CIOTAT



At the end, you should have a liste like:

ACCARDO MARIE-JOELLE( Madame )
13600      LA CIOTAT
181 AV DE LA MEDITERRANEELOTISSEMENT LES PHILIPPINESN°604.42.73.06.22
06 13 19 82 52
Journée4 enfant(s) De 0 à 6 ans dont un de plus de 18moisValide du 05/05/2004 au 04/05/2024
ACHI MAMMA ( Madame )
13600      LA CIOTAT
5 RUE KERGUELENPROVENCE 1 2 3 BT J09.51.88.27.9107.86.26.62.84
Journée2 enfant(s) De 0 à 6 ansValide du 14/12/2000 au 13/12/2020
AHSENE DJABALLAHLOUISA ( Madame )
13600      LA CIOTAT
