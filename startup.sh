python3 -m venv ./venv && source ./venv/Scripts/activate
pip install -r requirements.txt
python3 -m flask db init 
python3 -m flask db migrate -m "Initial-migration"
python3 -m flask db upgrade
cd client
npm i 
npm run build