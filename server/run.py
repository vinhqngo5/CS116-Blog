import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

server = create_app()



server.run(host=os.environ['HOST'], port=os.environ['PORT'], debug=os.environ['DEBUG'])

