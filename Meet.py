class Meet:
	
	def __init__(self, meet_name, date, meet_url, results):
		self.meet_name = meet_name
		self.date = date
		self.meet_url = meet_url
		self.results = results #{athlete object : (place, time)}
		self.result_list = [athlete.id for athlete in results]

	def compare(self, a1, a2):
		return self.results[a1][1] - self.results[a2][1]

	def __eq__(self, other):
		return self.meet_url == other.meet_url

	def __hash__(self):
		return hash(self.meet_url)


