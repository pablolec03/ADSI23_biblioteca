from . import BaseTestClass

class TestCatalogo(BaseTestClass):
	
	def test_online(self):
		res = self.client.get('/catalogue')
		self.assertEqual(200, res.status_code)
		self.assertIn(b'<div class="card d-flex flex-row" style="width: 18rem;"', res.data)


	def test_busquedaFallida(self):
		params = {
			'title': "Este libro no existe"
		}
		res = self.client.get('/catalogue', query_string = params)
		self.assertEqual(200, res.status_code)
		self.assertNotIn(b'<div class="card d-flex flex-row" style="width: 18rem;"', res.data)

	def test_busquedaHarryPotter(self):
		params = {
			'title': "Harry Potter"
		}
		res = self.client.get('/catalogue', query_string = params)
		self.assertIn(b'page=1"', res.data)
		self.assertIn(b'page=2"', res.data)
		self.assertNotIn(b'page=3"', res.data)


		



