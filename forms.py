from .models import Task2
from django.forms import ModelForm, NumberInput, Select, DateInput

class Task2Form(ModelForm):
	class Meta:
		
		model = Task2
		
		fields = ["city", "inhabitants", "shower_use", "water_usage_norm", "bath_use", "bath_temperature", 
				"shower_temperature", "tank_temperature", "time_of_tank_heating", "heat_losses_of_building", 
				"house_area", "air_temperature", "taryph", "enter_temperature", "exit_temperature", 
				"vugil_am", "vugil_cost", "gas_am", "gas_cost", "drowa_am", "drowa_cost", "pelet_am", "pelet_cost",
				"elec_am", "elec_cost"]
				
		widgets = {"city": Select(attrs={
						'class': 'form-control'
				  }), 
					"inhabitants": NumberInput(attrs={
						'class': 'form-control'
				  }), 
				  "shower_use": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "water_usage_norm": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "bath_use": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "bath_temperature": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "shower_temperature": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "tank_temperature": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "time_of_tank_heating": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "heat_losses_of_building": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "house_area": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "air_temperature": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "taryph": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "enter_temperature": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "exit_temperature": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "vugil_am": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "vugil_cost": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "gas_am": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "gas_cost": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "drowa_am": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "drowa_cost": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "pelet_am": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "pelet_cost": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "elec_am": NumberInput(attrs={
						'class': 'form-control'
				  }),
				  "elec_cost": NumberInput(attrs={
						'class': 'form-control'
				  })
		}