from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode
import mysql.connector
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import csv
import pandas as pd

cnx = mysql.connector.connect(user='root', password='Masuodakg1300',
                              host='127.0.0.1',
                              database='ml_car')
cursor = cnx.cursor()
for i in range(10):
    req = requests.get('https://mashinbank.com/%D8%AE%D8%B1%DB%8C%D8%AF-%D8%AE%D9%88%D8%AF%D8%B1%D9%88?kms=1000000&page={}'.format(i))
    soup = BeautifulSoup(req.text, 'html.parser')
    car_a = soup.find_all('a', attrs={'class' : 'cars-item-card'})
    for car in range(len(car_a)):
        car = car_a[car]
        car_link = re.findall(r'href=[\'\"]?([^\'\">]+)',str(car))
        req_page = requests.get('https://mashinbank.com{}'.format(car_link[0]))
        soup_page = BeautifulSoup(req_page.text, 'html.parser')
        car_price_class = soup_page.find('p',attrs={'class':'car-price'}).text
        car = re.sub(r'\s+',' ',car_price_class)
        car_en = unidecode(car)
        p_car = re.sub(r',','',car_en)
        price = re.findall(r'.* : (\d*)',p_car)
        if price != ['']:

            car_info = soup_page.find('div', attrs={'class':'row car-info'})
            car_func = re.findall(r'<span.([^\>]+)</span>',str(car_info))
            a = unidecode(car_func[0])
            car_inf = re.sub(r',','',a)
            

            car_details = soup_page.find('ul', attrs={'class':'car-details'})
            car_detail = re.findall(r'span.([^\>]+)</span>', str(car_details))
            en_cylinder = unidecode(car_detail[3])
            Cylinder_number = re.findall(r'\d+',en_cylinder)


            cursor.execute('INSERT INTO car_info VALUES (\'%i\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%i\',\'%s\',\'%s\',\'%i\')' % (int(car_inf),car_func[1],car_func[2],car_detail[0],car_detail[1],car_detail[2],int(Cylinder_number[0]),car_detail[4],car_detail[5],int(price[0])))
            cnx.commit()

query = ('SELECT * FROM car_info')
cursor.execute(query)
alldata = cursor.fetchall()
all_Func = []
all_Color = []
all_Body_condition = []
all_Color_inside = []
all_Chassis_type = []
all_gearbox = []
all_Cylinder_number = []
all_fuel_type = []
all_License_plate_type = []
all_Price = []
for Func ,Color ,Body_condition ,Color_inside ,Chassis_type ,gearbox ,Cylinder_number ,fuel_type ,License_plate_type ,Price in alldata:
    all_Func.append(Func)
    all_Color.append(Color)
    all_Body_condition.append(Body_condition)
    all_Color_inside.append(Color_inside)
    all_Chassis_type.append(Chassis_type)
    all_gearbox.append(gearbox)
    all_Cylinder_number.append(Cylinder_number)
    all_fuel_type.append(fuel_type)
    all_License_plate_type.append(License_plate_type)
    all_Price.append(Price)
dic = {'Func':all_Func ,'Color':all_Color ,'Body_condition':all_Body_condition ,'Color_inside':all_Color_inside ,'Chassis_type':all_Chassis_type ,'gearbox':all_gearbox ,'Cylinder_number':all_Cylinder_number ,'fuel_type':all_fuel_type ,'License_plate_type':all_License_plate_type ,'Price':all_Price}
df = pd.DataFrame(dic)
df_csv = df.to_csv('E:/cars_info.csv')
df1 = pd.read_csv('E:/cars_info.csv')
inputs = df1.drop('Price',axis = 'columns')
target = df1['Price']

le_Color = LabelEncoder()
le_Body_condition = LabelEncoder()
le_Color_inside = LabelEncoder()
le_Chassis_type = LabelEncoder()
le_gearbox = LabelEncoder()
le_Cylinder_number = LabelEncoder()
le_fuel_type = LabelEncoder()
le_License_plate_type = LabelEncoder()

inputs['Color_n'] = le_Color.fit_transform(inputs['Color'])
inputs['Body_condition_n'] = le_Body_condition.fit_transform(inputs['Body_condition'])
inputs['Color_inside_n'] = le_Color_inside.fit_transform(inputs['Color_inside'])
inputs['Chassis_type_n'] = le_Chassis_type.fit_transform(inputs['Chassis_type'])
inputs['gearbox_n'] = le_gearbox.fit_transform(inputs['gearbox'])
inputs['Cylinder_number_n'] = le_Cylinder_number.fit_transform(inputs['Cylinder_number'])
inputs['fuel_type_n'] = le_fuel_type.fit_transform(inputs['fuel_type'])
inputs['License_plate_type_n'] = le_License_plate_type.fit_transform(inputs['License_plate_type'])

inputs_n = inputs.drop(['Func','Color','Body_condition','Color_inside','Chassis_type','gearbox','Cylinder_number','fuel_type','License_plate_type','Unnamed: 0'],axis='columns')

model = tree.DecisionTreeClassifier()
model = model.fit(inputs_n,target)

new_data = [[4,2,3,1,1,0,0,0]]
answer = model.predict(new_data)
print(answer[0])
