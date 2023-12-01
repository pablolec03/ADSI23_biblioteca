from . import BaseTestClass

class TestLogin(BaseTestClass):

	def test_login_page_unauthentificated(self):
		res = self.client.get('/login')
		self.assertEqual(200, res.status_code)
		self.assertIn(b'<input type="email" id="email" name="email" class="form-control mb-2"', res.data)
		self.assertIn(b'<input type="password" id="password" name="password" class="form-control mb-2"', res.data)
		self.assertIn(b'<button type="submit" class="btn btn-primary btn-block mb-4"', res.data)

	def test_login_success(self):
		res = self.login('jhon@gmail.com', '123')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/', res.location)

	def test_login_failure(self):
		res = self.login('jhon@gmail.com', 'badpassword')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/login', res.location)

