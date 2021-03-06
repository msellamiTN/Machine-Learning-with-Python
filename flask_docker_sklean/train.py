# -*- coding: utf-8 -*-
"""Machine Learning with Python - Day 4 - Lab 3 - Model Serving - Logistic Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VDOAepI41_IH-8jduUJh2wyA0p7Y0Jyt

<h1 align="center"><font size="5"> Logistic Regression with Python</font></h1>

Dans ce cahier, vous apprendrez la régression logistique, puis vous créerez un modèle pour une entreprise de télécommunications, pour prédire quand ses clients partiront pour un concurrent, afin qu'ils puissent prendre des mesures pour fidéliser les clients.

<h1>Table des matières</h1>

<div class="alert alert-block alert-info" style="margin-top: 20px">
    <ol>
        <li><a href="#about_dataset">À propos du dataset</a></li>
        <li><a href="#preprocessing">Prétraitement et sélection des données</a></li>
        <li><a href="#modeling">Modélisation (régression logistique avec Scikit-learn) </a></li>
        <li><a href="#evaluation">Evaluation</a></li>
        <li><a href="#practice">Practice</a></li>
    </ol>
</div>
<br>
<hr>

### Customer churn with Logistic Regression

Une entreprise de télécommunications est préoccupée par le nombre de clients qui quittent leur entreprise de téléphonie fixe pour des concurrents du câble. Ils ont besoin de comprendre qui part. Imaginez que vous êtes analyste dans cette entreprise et que vous devez savoir qui part et pourquoi.

Permet d'abord d'importer les bibliothèques requises:
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import pylab as pl
import numpy as np
import scipy.optimize as opt
from sklearn import preprocessing
# %matplotlib inline 
import matplotlib.pyplot as plt

"""<h2 id="about_dataset">À propos du dataset</h2>
Nous utiliserons un ensemble de données de télécommunications pour prédire le taux de désabonnement des clients. Il s'agit d'un ensemble de données client historique où chaque ligne représente un client. Les données sont relativement faciles à comprendre et vous pouvez découvrir des informations que vous pouvez utiliser immédiatement. En règle générale, il est moins coûteux de conserver des clients que d'en acquérir de nouveaux. L'objectif de cette analyse est donc de prédire les clients qui resteront dans l'entreprise.


Cet ensemble de données fournit des informations pour vous aider à prédire quel comportement vous aidera à fidéliser vos clients. Vous pouvez analyser toutes les données client pertinentes et développer des programmes de fidélisation client ciblés.



L'ensemble de données comprend des informations sur:

- Clients qui sont partis au cours du dernier mois - la colonne est appelée Churn
- Services auxquels chaque client s'est abonné - téléphone, lignes multiples, Internet, sécurité en ligne, sauvegarde en ligne, protection de l'appareil, assistance technique et diffusion de programmes télévisés et de films
- Informations sur le compte client - depuis combien de temps il est client, contrat, mode de paiement, facturation sans papier, frais mensuels et total des frais
- Informations démographiques sur les clients - sexe, tranche d'âge et s'ils ont des partenaires et des personnes à charge

### Charger les données de désabonnement Telco
Telco Churn est un fichier de données hypothétique qui concerne les efforts d'une entreprise de télécommunications pour réduire le chiffre d'affaires de sa clientèle. Chaque cas correspond à un client distinct et enregistre diverses informations démographiques et d'utilisation des services. Avant de pouvoir travailler avec les données, vous devez utiliser l'URL pour obtenir le fichier ChurnData.csv.

Pour télécharger les données, nous utiliserons `! Wget` pour les télécharger depuis IBM Object Storage.
"""

#Click here and press Shift+Enter
!wget -O ChurnData.csv https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/ChurnData.csv

"""### Load Data From CSV File  """

churn_df = pd.read_csv("ChurnData.csv")
churn_df.head()

"""<h2 id="preprocessing">Prétraitement et sélection des données</h2>

Permet de sélectionner certaines fonctionnalités pour la modélisation. Nous changeons également le type de données cible en entier, car c'est une exigence de l'algorithme skitlearn:
"""

churn_df = churn_df[['tenure', 'age', 'address', 'income', 'ed', 'employ', 'equip',   'callcard', 'wireless','churn']]
churn_df['churn'] = churn_df['churn'].astype('int')
churn_df.head()

"""Définissons X et y pour notre ensemble de données:"""

X = np.asarray(churn_df[['tenure', 'age', 'address', 'income', 'ed', 'employ', 'equip']])
X[0:5]

y = np.asarray(churn_df['churn'])
y [0:5]

"""De plus, nous normalisons l'ensemble de données:"""



from sklearn import preprocessing
X = preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]

"""## Train/Test dataset

D'accord, nous avons divisé notre ensemble de données en train et ensemble de test:
"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

"""<h2 id="modeling">Modeling (Logistic Regression with Scikit-learn)</h2>

Permet de construire notre modèle en utilisant __LogisticRegression__ à partir du package Scikit-learn. Cette fonction implémente la régression logistique et peut utiliser différents optimiseurs numériques pour trouver des paramètres, y compris les solveurs «newton-cg», «lbfgs», «liblinear», «sag», «saga». Vous pouvez trouver des informations détaillées sur les avantages et les inconvénients de ces optimiseurs si vous les recherchez sur Internet.

La version de la régression logistique dans Scikit-learn prend en charge la régularisation. La régularisation est une technique utilisée pour résoudre le problème de surajustement dans les modèles d'apprentissage automatique.
Le paramètre __C__ indique __l'inverse de la force de régularisation__ qui doit être un flottant positif. Des valeurs plus petites indiquent une régularisation plus forte.
Maintenant, adaptons notre modèle avec ensemble de train:
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_train,y_train)
LR

"""Maintenant, nous pouvons prédire en utilisant notre ensemble de test:"""

yhat = LR.predict(X_test)
yhat

"""__predict_proba__ retourne des estimations pour toutes les classes, triées par l'étiquette des classes. Ainsi, la première colonne est la probabilité de classe 1, P(Y=1|X), et la deuxième colonne est la probabilité de classe 0, P(Y=0|X):"""

yhat_prob = LR.predict_proba(X_test)
yhat_prob

"""<h2 id="evaluation">Serialisation du Modèle avec Pickle </h2>
Pickle : une bibliothèque de sérialisation Python standard utilisée pour enregistrer les modèles de scikit-learn
"""

# Load libraries
import pickle
from sklearn.externals import joblib
# Save the trained model as a pickle string.
saved_model = pickle.dumps(LR)

# Save the model as a pickle in a file
joblib.dump(LR, 'chrunlog_r.pkl')