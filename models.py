from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import re
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import mplcursors
import time
from collections import Counter
import pandas as pd
import math
import xlrd
from datetime import time, datetime, date
import numpy as np
import plotly 
import io
from io import BytesIO
import base64
import mpld3


CITY_DICT = [(-23, "Дніпро"), 
			 (-23, "Донецьк"), 
			 (-20, "Івано-Франківськ"), 
			 (-22, "Київ"), 
			 (-23, "Кривий ріг"), 
			 (-25, "Луганськ"), 
			 (-19, "Львів"), 
			 (-16, "Симферополь"), 
			 (-18, "Одеса"), 
			 (-23, "Харків")]
	
cities_ukr = ['Дніпро', 'Донецьк', 'Івано-Франківськ', 'Київ', 
              'Кривий Ріг', 'Луганськ', 'Львів', 'Сімферополь', 'Одеса', 
              'Харків']	

temps = [-23, -23, -20, -22, -23, -25, -19, -16, -18, -23]
			  
dic_t_out = dict(zip(cities_ukr, temps))
#{"Дніпро":-23, "Донецьк":-23, "Івано-Франківськ":-20, "Київ":-22, "Кривий Ріг":-23, "Луганськ":-25, "Львів":-19, "Симферополь":-16, "Одеса":-18, "Харків":-23}
	
cities = dict(zip(cities_ukr, ['Dnepr', 'Donetsk', 'I_Frankivsk', 'Kyiv', 
                                 'Krivy_Rig', 'Luhansk', 'Lviv',  
                                 'Simferopol', 'Odessa', 'Kharkiv']))

	
# Create your models here.
class Task2(models.Model):
	city = models.FloatField(choices=CITY_DICT, default=-22)

	choice1 = models.IntegerField(default=11)
	choice2 = models.IntegerField(default=12)
	m_x2 = models.IntegerField(default=21)
	
	inhabitants = models.IntegerField(default=1)
	shower_use = models.IntegerField(default=1)
	water_usage_norm = models.FloatField(default=100.0)
	bath_use = models.FloatField(default=1.0)
	bath_temperature = models.FloatField(default=37.0)
	shower_temperature = models.FloatField(default=30.0)
	tank_temperature = models.FloatField(default=60.0)
	time_of_tank_heating = models.FloatField(default=120.0)
	heat_losses_of_building =models.FloatField(default=0.0839)
	house_area = models.FloatField(default=75.0, validators=[MinValueValidator(0.0), MaxValueValidator(2000)])
	air_temperature = models.FloatField(default=20.0)
	air_temperature_out = models.FloatField(choices=CITY_DICT, default=-22)
	
	taryph = models.FloatField(default=1444.0)
	enter_temperature = models.FloatField(default=15.0)
	exit_temperature = models.FloatField(default=85.0)
	time_vol_heating = models.FloatField(default=10.0)
	
	vugil_am = models.FloatField(default=0.0001782)
	vugil_cost = models.FloatField(default=4234)
	gas_am = models.FloatField(default=0.1065)
	gas_cost = models.FloatField(default=5.97)
	drowa_am = models.FloatField(default=0.000387)
	drowa_cost = models.FloatField(default=850)
	pelet_am = models.FloatField(default=0.0001893)
	pelet_cost = models.FloatField(default=4650)
	elec_am = models.FloatField(default=1.01)
	elec_cost = models.FloatField(default=1.68)
	
	@property
	def cit(self):
		for k, v in dic_t_out.items():
			if v == int(self.city):
				return k

	@property
	def set_temp(self):
		self.air_temperature_out = self.city
		return ''
				
	@property
	def func1(self):
		return round(self.shower_use * self.inhabitants * self.water_usage_norm, 5)
	
	@property
	def func2(self):
		return round(self.bath_use * self.inhabitants * self.water_usage_norm * 1.325, 5)
	
	@property
	def func3(self):
		return round((self.func1) * ((self.shower_temperature - self.enter_temperature)/(self.exit_temperature - self.enter_temperature)), 5)
		
	@property
	def func4(self):
		return round(self.func2 * ((self.bath_temperature - self.enter_temperature)/(self.exit_temperature - self.enter_temperature)), 5)
		
	@property
	def func5(self):
		return round((self.func3+self.func4)/(992.2844), 5)
		
	@property
	def func6(self):
		return round(1.163*self.func5*(self.tank_temperature - self.enter_temperature), 5)
		
	@property
	def func7(self):
		return round(60*(self.func6/self.time_of_tank_heating), 5)
	
	@property
	def func8_1(self):
		return round(self.heat_losses_of_building, 5)#(self.air_temperature - self.air_temperature_out)*1.163
	
	@property
	def func8(self):
		if (self.inhabitants == 1) and (self.shower_use == 2) and (self.bath_use == 1):
			self.choice1 = 10
			self.choice2 = 11
			self.m_x2 = 25
		
		if (self.inhabitants == 1) and self.shower_use == 1 and self.bath_use == 2:
			self.choice1 = 10
			self.m_x2 = 25
		
		return round(self.heat_losses_of_building * self.house_area, 5)
		
	
	
	def cons_temp(self):
		

		db = []
		#Считывание и вывод БД
		#Замена пропусков
		def autocorrection(db1):  
			l1 = db1['Число месяца'].tolist()
			l2 = db1['UTC'].tolist()
			l3 = db1['T'].tolist()
			l4 = db1['dd'].tolist()
			l5 = db1['FF'].tolist()
			
		   
			for i in range(len(l1)): 
				if l1[i]!=l1[i]: 
					if i+1 < len(l1): l1[i] = l1[i-1] if l1.count(l1[i-1]) < 48 else l1[i-1]+1
					l1[i] = l1[i-1]
						
				if l2[i]!=l2[i]: 
					l2[i] = l2[i-1].minute + time(0, 30).minute
				
				if l3[i]!=l3[i]:
					if i+1 < len(l3):
						l3[i] = l3[i-1] if l3.count(l3[i-1]) < 48 else l3[i-1]+1
					l3[i] = l3[i-1]
				
				if l4[i]!=l4[i]: 
					l4[i] = "Штиль"
				
				if l5[i]!=l5[i]: 
					l5[i] = int(input("Введіть середню швидкість вітру (невід'ємну): "))
				if l5[i] < 0: 
					l5[i] = -l5[i]
			
			return [l1, l2, l3, l4, l5]

				
		#Считывание БД
		for i in range(self.choice1, self.choice2):
			db.append(pd.read_excel('https://github.com/anton-kachur/weather/blob/'+cities[self.cit]+'/2012-'+str(i)+'.xlsx?raw=true', usecols=range(0, 5)))
			
		for j, i in enumerate(db):
			db[j] = autocorrection(i)
			

		x2 = []
		y2 = []
		base = []

		[[base.append(int(i)) for i in db[k][2]] for k in range(self.choice2-self.choice1)]

		for a, b in Counter(base).items():
			#print(a, "->", b)
			x2.append(int(a))
			y2.append((b*30)/60)
			
		
		k = (self.heat_losses_of_building * self.house_area - 0) / (self.air_temperature_out - 20)
		b = 0 - k * 20
		
		
		
		x = range(int(self.air_temperature_out), self.m_x2)
		y = []
		for i in x:
			y.append(k*i+b)
		
	
		summ = []
		
		jj=0
		
		for i in x2:
			if i in x:
				summ.append((k*i+b)*y2[jj])
				jj+=1
		
		return round(sum(summ), 5)
		
		
		
	def get_Graph_lab2(self):
		fig, ax = plt.subplots(figsize=(10,5), dpi = 100)
		plt.xlabel("T(С°)") # ось абсцисс
		plt.ylabel("Q (кВт)") # ось ординат
		# plt.grid()      # включение отображение сетки
		
		k = (self.heat_losses_of_building * self.house_area - 0) / (self.air_temperature_out - 20)
		b = 0 - k * 20
		
		
		x = range(int(self.air_temperature_out), self.m_x2)
		y = []
		for i in x:
			y.append(k*i+b)

		Teplovtrata_time = {}
			
		for i in range(len(x)):
			Teplovtrata_time = dict(zip(x, y)) 

		p = 'y = '+str(float(f"{k:.{2}f}"))+'x + '+str(float(f"{b:.{2}f}"))
		plt.plot((self.air_temperature_out, 20),(self.heat_losses_of_building*self.house_area, 0))
	
		
		plt.title("Залежність тепловтрат будівлі від температурних умов \nQ = " + str(float(f"{k:.{2}f}")) + "t + " + str(float(f"{b:.{2}f}"))) # заголовок
		
		plt.axvline(x=0, color='black', linewidth=0.2)

		if self.air_temperature != 20:
			y_ = list(range(int(self.air_temperature_out), 21))
			y1 = []

			for i in range(0, len(y_)):
				if self.air_temperature < 20:
					y_[i] -= (20 - self.air_temperature)
				else:
					y_[i] += (self.air_temperature - 20)

			k = (self.heat_losses_of_building*self.house_area - 0) / (self.air_temperature_out - y_[0])
			b = 0 - k * y_[0]

			for i in y_:
				y1.append(k*i+b)

			scat1 = plt.scatter(y_, y, marker = 'o', c = 'green', edgecolors = 'black',alpha = 0.6)
			plt.plot((y_[0], self.air_temperature),(self.heat_losses_of_building*self.house_area, 0), c='green')

		def fig_to_base64(fig):
			img = io.BytesIO()
			fig.savefig(img, format='png',
						bbox_inches='tight')
			img.seek(0)

			return base64.b64encode(img.getvalue())
		
		encoded = fig_to_base64(fig)
		my_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
		return my_html
		
		
	
	def set_bd1(self):
		db = []

		#Считывание и вывод БД

		#Замена пропусков
		def autocorrection(db1):  
			l1 = db1['Число месяца'].tolist()
			l2 = db1['UTC'].tolist()
			l3 = db1['T'].tolist()
			l4 = db1['dd'].tolist()
			l5 = db1['FF'].tolist()
			
		   
			for i in range(len(l1)): 
				if l1[i]!=l1[i]: 
					if i+1 < len(l1): l1[i] = l1[i-1] if l1.count(l1[i-1]) < 48 else l1[i-1]+1
					l1[i] = l1[i-1]
						
				if l2[i]!=l2[i]: 
					l2[i] = l2[i-1].minute + time(0, 30).minute
				
				if l3[i]!=l3[i]:
					if i+1 < len(l3):
						l3[i] = l3[i-1] if l3.count(l3[i-1]) < 48 else l3[i-1]+1
					l3[i] = l3[i-1]
				
				if l4[i]!=l4[i]: 
					l4[i] = "Штиль"
				
				if l5[i]!=l5[i]: 
					l5[i] = int(input("Введіть середню швидкість вітру (невід'ємну): "))
				if l5[i] < 0: 
					l5[i] = -l5[i]
			
			return [l1, l2, l3, l4, l5]

				
		#Считывание БД
		
		
		for i in range(self.choice1, self.choice2):
			db.append(pd.read_excel('https://github.com/anton-kachur/weather/blob/'+cities[self.cit]+'/2012-'+str(i)+'.xlsx?raw=true', usecols=range(0, 5)))
			
		for j, i in enumerate(db):
			db[j] = autocorrection(i)
			

		x2 = []
		y2 = []
		base = []

		[[base.append(int(i)) for i in db[k][2]] for k in range(self.choice2-self.choice1)]

		for a, b in Counter(base).items():
			#print(a, "->", b)
			if (int(a) <= 20):
				x2.append(int(a))
				y2.append((b*30)/60)

			
		def autolabel(rects, labels=None, height_factor=1.01):
			for i, rect in enumerate(rects):
				height = rect.get_height()
				if labels is not None:
					try:
						label = labels[i]
					except (TypeError, KeyError):
						label = ' '
				else:
					label = '%d' % int(height)
				axes.text(rect.get_x() + rect.get_width()/2., height_factor*height,
						'{}'.format(label),
						ha='center', va='bottom', fontsize = 12)
		
		
		def fig_to_base64(fig):
			img = io.BytesIO()
			fig.savefig(img, format='png',
						bbox_inches='tight')
			img.seek(0)

			return base64.b64encode(img.getvalue())
		
	
		d = sorted(zip(x2, y2), key = lambda t: t[0])
				
		#Вывод диаграммы
		fig, axes = plt.subplots()
		plt.title("Тривалість температурних режимів за визначений період")
		axes.bar(x2, y2, color="#009933", width=0.5)
		autolabel(axes.patches, height_factor=1.02)
		
		fig.set_figwidth(10)    #  ширина Figure
		fig.set_figheight(5)    #  высота Figure
		plt.xlabel("T,\n(°C)")
		plt.yticks([])
		plt.xticks(np.arange(min(x2), max(x2)+1, 1))
		axes.xaxis.set_label_coords(0.00, -0.025)
		
		
	
		encoded1 = fig_to_base64(fig)
		my_html1 = '<img src="data:image/png;base64, {}">'.format(encoded1.decode('utf-8'))
		return my_html1
	
    
	
	def set_bd2(self):
		db = []

		#Считывание и вывод БД

		#Замена пропусков
		def autocorrection(db1):  
			l1 = db1['Число месяца'].tolist()
			l2 = db1['UTC'].tolist()
			l3 = db1['T'].tolist()
			l4 = db1['dd'].tolist()
			l5 = db1['FF'].tolist()
			
		   
			for i in range(len(l1)): 
				if l1[i]!=l1[i]: 
					if i+1 < len(l1): l1[i] = l1[i-1] if l1.count(l1[i-1]) < 48 else l1[i-1]+1
					l1[i] = l1[i-1]
						
				if l2[i]!=l2[i]: 
					l2[i] = l2[i-1].minute + time(0, 30).minute
				
				if l3[i]!=l3[i]:
					if i+1 < len(l3):
						l3[i] = l3[i-1] if l3.count(l3[i-1]) < 48 else l3[i-1]+1
					l3[i] = l3[i-1]
				
				if l4[i]!=l4[i]: 
					l4[i] = "Штиль"
				
				if l5[i]!=l5[i]: 
					l5[i] = int(input("Введіть середню швидкість вітру (невід'ємну): "))
				if l5[i] < 0: 
					l5[i] = -l5[i]
			
			return [l1, l2, l3, l4, l5]

				
		#Считывание БД
		for i in range(self.choice1, self.choice2):
			db.append(pd.read_excel('https://github.com/anton-kachur/weather/blob/'+cities[self.cit]+'/2012-'+str(i)+'.xlsx?raw=true', usecols=range(0, 5)))
			
		for j, i in enumerate(db):
			db[j] = autocorrection(i)
			

		x2 = []
		y2 = []
		base = []

		[[base.append(int(i)) for i in db[k][2]] for k in range(self.choice2-self.choice1)]

		for a, b in Counter(base).items():
			#print(a, "->", b)
			x2.append(int(a))
			y2.append((b*30)/60)

		def fig_to_base64(fig):
			img = io.BytesIO()
			fig.savefig(img, format='png',
						bbox_inches='tight')
			img.seek(0)

			return base64.b64encode(img.getvalue())
		
	
		d = sorted(zip(x2, y2), key = lambda t: t[0])
				
		
		
		#сумма всех затрат
		sum_of_all = 0.0
		for a, b in Counter(base).items():
			#print(a, "->", b)
			sum_of_all += (((-0.15*int(a)) + 3.0) * 1000 * (b*30)/60)
		
		sum_of_all_1 = (sum_of_all*859.845)
		
		
		x3 = ["Централізована мережа", "Вугільний котел", "Газовий котел", "Дров'яний котел", "Пелетний котел", "Елетричний котел"]
		y3 = [(sum_of_all_1*self.taryph)/1000000, sum_of_all*self.vugil_am*self.vugil_cost, sum_of_all*self.gas_am*self.gas_cost, 
			  sum_of_all*self.drowa_am*self.drowa_cost, sum_of_all*self.pelet_am*self.pelet_cost, sum_of_all*self.elec_cost]
		
		
		#второй график
		f, a = plt.subplots()
		plt.title("Вартість опалення для всіх типів енергозабезпечення\nЗагальні витрати енергії по всім режимам: {}(кВт*год)".format(sum_of_all/1000))
		a.bar(x3, y3, color="#009933", width=0.5)
		
		f.set_figwidth(10)    #  ширина Figure
		f.set_figheight(5)    #  высота Figure
		
		plt.ylabel("Вартість (тис. грн)")
		
		plt.xticks(np.arange(0, len(x3)+1, 1))
		locs, labels = plt.xticks()
		plt.setp(labels, rotation=30)
		a.xaxis.set_label_coords(0.00, -0.025)
	
		encoded2 = fig_to_base64(f)
		my_html2 = '<img src="data:image/png;base64, {}">'.format(encoded2.decode('utf-8'))
		return my_html2