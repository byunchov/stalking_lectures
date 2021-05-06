# stalking_lectures

Requirements before running server:
1. Install Python (3.9.5 used for this project)
2. Install virtualenv -> environment used for this project so you don't install all dependencies on your system
```pip3 install virtualenv```
3. Go to project directory and create your virtualenv
```virtualenv env```
4. Start virtual environment:
- Mac/Linux:
```source ./env/bin/activate```
- Windows:
```env\Scripts\activate.bat```
5. Install requirements with:
```pip3 install -r requirements.txt```
6. Run server:
```python3 manage.py runserver```