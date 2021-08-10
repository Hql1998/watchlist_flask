import unittest

from main import app, db, Novel, User, forge, initdb

class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()
        user = User(name="Test", username="test")
        user.set_password("123")
        novel = Novel(title="Novel Test", year="2019")

        db.session.add_all([user, novel])
        db.session.commit()

        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner() # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config["TESTING"])

    def login(self):
        response = self.client.post("/login", data=dict(
            username="test",
            password="123"
        ), follow_redirects=True
        )

    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Login success.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)

    def test_create_item(self):

        self.login()

        # valid novel creation input
        response = self.client.post("/", data=dict(
            name="New Novel",
            year="1998"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("item added!", data)
        self.assertIn("New Novel", data)

        #invlide input title is empty
        response = self.client.post('/', data=dict(
            title='',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('item added!', data)
        self.assertIn('invalid input', data)

        #invlide input year is empty
        response = self.client.post('/', data=dict(
            title='New Novel1',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('item added!', data)
        self.assertIn('invalid input', data)

    def test_update_item(self):
        self.login()

        #test editing page
        response = self.client.get("/edit_novel/id_1")
        data = response.get_data(as_text=True)
        self.assertIn('Edit Item', data)
        self.assertIn('Novel Test', data)
        self.assertIn('2019', data)

        #test update the input
        response = self.client.post("/edit_novel/id_1", data=dict(
            title="New Novel Edited",
            year="2008"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Item updated", data)
        self.assertIn('New Novel Edited', data)

    def test_delete_item(self):
        self.login()

        response = self.client.post('/delete_novel/id_1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted', data)
        self.assertNotIn('Test Movie Title', data)

    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)



    def test_logout(self):
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)

    def test_settings(self):
        self.login()

        # 测试设置页面
        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(
            name='Grey Li',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings updated.', data)
        self.assertIn('Grey Li', data)

    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('database forged', result.output)
        self.assertNotEqual(Novel.query.count(), 0)

    # 测试初始化数据库
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

    # 测试生成管理员账户
    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(args=['admin', '--username', 'grey', '--password', '123'])
        self.assertIn('Creating user ...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'grey')
        self.assertTrue(User.query.first().validate_password('123'))

    # 测试更新管理员账户
    def test_admin_command_update(self):
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(args=['admin', '--username', 'peter', '--password', '456'])
        self.assertIn('Updating user ...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'peter')
        self.assertTrue(User.query.first().validate_password('456'))


if __name__ == '__main__':
    unittest.main()