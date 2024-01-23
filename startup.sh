npm i
pip install -r requirements.txt
python -m flask db init 
python -m flask db migrate "Initial-migration"
python -m flask db upgrade
cd client
npm run build
