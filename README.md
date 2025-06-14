 # Solana Wallet Dashboard

Un dashboard minimaliste pour analyser les soldes des wallets Solana.

## Installation

### Frontend (React + TypeScript + Tailwind)

1. Installer les dépendances :
```bash
npm install
```

2. Démarrer le serveur de développement :
```bash
npm start
```

### Backend (Python + FastAPI)

1. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Démarrer le serveur backend :
```bash
cd backend
python main.py
```

## Utilisation

1. Ouvrez l'application dans votre navigateur à l'adresse `http://localhost:3000`
2. Collez vos adresses de wallet Solana au format JSON dans la zone de texte
3. Cliquez sur "Analyze" pour voir le leaderboard des soldes

## Format JSON attendu

```json
[
  "wallet_address_1",
  "wallet_address_2",
  "wallet_address_3"
]
```"# dashboard-solana" 
