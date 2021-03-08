from .models import Task
from main.forms import ModelForm

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ["inhabitants", "shower_use"]