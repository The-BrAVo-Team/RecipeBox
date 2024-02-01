echo "Creating and selecting virtual environment"
python3 -m venv ./venv && source ./venv/Scripts/activate
echo "Instaling requirements"
pip install -r requirements.txt
echo "Initalizing flask db"
python3 -m flask db init 
echo "Starting flask migration"
python3 -m flask db migrate -m "Initial-migration"
echo "upgrading flask db"
python3 -m flask db upgrade
echo "installing node dependencies and running build"
cd client
npm i 
npm run build