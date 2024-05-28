import os
import pytest
from app import app, db, CURR_USER_KEY
from models import User, BoardGame

os.environ['DATABASE_URL'] = "postgresql:///test_warbler"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def setup_user(client):
    """Setup a sample user for testing."""
    user = User.signup(username="testuser", password="testpass", email="test@example.com", location="testlocation")
    db.session.commit()
    return user

def login(client, username, password):
    """Helper function to log in a user."""
    return client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

def logout(client):
    """Helper function to log out a user."""
    return client.get('/logout', follow_redirects=True)

def test_signup(client):
    """Test user signup."""
    response = client.post('/signup', data={
        'username': 'newuser',
        'password': 'newpass',
        'email': 'newuser@example.com',
        'location': 'newlocation',
        'image_url': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter_by(username='newuser').first()
    assert user is not None

def test_login_logout(client, setup_user):
    """Test user login and logout."""
    response = login(client, 'testuser', 'testpass')
    assert response.status_code == 200
    assert CURR_USER_KEY in client.session

    response = logout(client)
    assert response.status_code == 200
    assert CURR_USER_KEY not in client.session

def test_user_profile(client, setup_user):
    """Test user profile update."""
    login(client, 'testuser', 'testpass')
    response = client.post('/users/profile', data={
        'username': 'updateduser',
        'email': 'updated@example.com',
        'location': 'updatedlocation',
        'image_url': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    user = User.query.get(setup_user.id)
    assert user.username == 'updateduser'
    assert user.email == 'updated@example.com'



def test_add_remove_game(client, setup_user):
    """Test adding and removing a board game."""
    login(client, 'testuser', 'testpass')
    response = client.post('/users/add_games', data={
        'gamename': 'Chess'
    }, follow_redirects=True)
    assert response.status_code == 200
    game = BoardGame.query.filter_by(name='Chess').first()
    assert game is not None
    assert game in setup_user.boardgames

    response = client.post(f'/users/remove_game/{game.id}', follow_redirects=True)
    assert response.status_code == 200
    assert game not in setup_user.boardgames


def test_homepage_logged_in(client, setup_user):
    """Test homepage for logged-in user."""
    login(client, 'testuser', 'testpass')
    response = client.get('/')
    assert response.status_code == 200
    assert b"testuser" in  response.data

def test_homepage_logged_out(client):
    """Test homepage for logged-out user."""
    response = client.get('/')
    assert response.status_code == 200

    assert b"Sign up" in response.data
   
    assert b"Log in" in response.data

def test_user_following(client, setup_user):
    """Test following a user."""
    other_user = User.signup(username="otheruser", password="otherpass", email="other@example.com", location="otherlocation")
    db.session.commit()
    
    login(client, 'testuser', 'testpass')
    response = client.post(f'/users/{other_user.id}/follow', follow_redirects=True)
    assert response.status_code == 200
    assert other_user in setup_user.following

    response = client.post(f'/users/{other_user.id}/follow', follow_redirects=True)
    assert response.status_code == 200
    assert other_user not in setup_user.following
