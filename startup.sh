virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
python -m flask db init 
python -m flask db migrate -m "Initial-migration"
python -m flask db upgrade
cd client
npm i 
npm run build