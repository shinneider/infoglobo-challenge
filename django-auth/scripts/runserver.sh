pip install -r requirements.txt
python manage.py migrate

if [ "$VSCODE_DEBUG" == "yes" ];
then
  echo "debug enabled."
  pip install ptvsd
  python -m ptvsd --host 0.0.0.0 --port 5678 --wait manage.py runserver --noreload 0.0.0.0:8000
else
  python manage.py runserver 0:8000
fi