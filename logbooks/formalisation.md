# Formalisation  de la fonction de coût  
On cherche à la fois à limiter les temps d'arrêt aux intersections en contrôlant les feux tricolores et à limiter les émissions de polluant. On a convenu que les émissions de polluants pouvaient être approchées par la taille des vecteurs d'accélération des véhicules.  
Vu dans la littérature (Adaptive multi-objective reinforcement learning with hybrid exploration for traffic signal control based on cooperative multi-agent framework, Khamis et Gomaa, 2014 -> paper dans le Git), on peut cumuler plusieurs fonctions de coût répondant à des objectifs différents.  
On se propose, pour limiter l'accélération, d'utiliser un reward inversement proportionnel à la norme des vecteurs accélération des véhicules à l'intersection ; pour limiter le temps d'attente une pénalité si le véhicule s'arrête à l'intersection.  
Un reward pour un agent intersection peut être :

=== sum_i  - || text(acceleration)_i || + penalite_i ===  
avec i l'indice des véhicules présents à l'intersection. Le tableau de pénalités est à discuter.

Pour le contrôle de vitesse des véhicules, on propose de discrétiser les valeurs possibles. Par exemple : l'intersection envoie au véhicule qui entre dans la zone de capteurs une instruction vitesse :
```
- variation 0km/h
- variation -5km/h
- ...
- borner la vitesse minimale des véhicules.
```  
L'intersection contrôle ainsi le moment d'arivée du véhicule au feu et peut optimiser le temps de feu vert.

## Question ouverte : comment on définit le moment auquel un véhicule 'entre' dans une intersection ? A quelle vitesse ?

# Contraintes

```
- temps de trajet inférieur ou égal à 1.5x fois le temps de trajet sans algo (valeur à discuter)
- borne inférieure et supérieure du temps de 'feu vert'
- vitesse maximale et minimale sur les routes
- temps de feu rouge minimal (piétons)
```

**Note :** dans le papier 'Hierarchical multi-agent control of traffic lights based on collective learning', Jin et Ma, ils proposent un algorithme de **reinforcement learning** SARSA (State - Action - Reward - State - Action) pour résoudre le problème. C'est une amélioration de celui de Q learning (prise en compte de l'instant t-1). On commence avec le Q learning ? Autre chose ?
