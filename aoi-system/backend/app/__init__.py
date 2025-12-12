"""Flask Application Factory"""
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'temp')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/aoi_system')

    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize database
    from app.database import Session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()

    # Register blueprints
    from app.routes.upload import bp as upload_bp
    from app.routes.process import bp as process_bp
    from app.routes.inspection import bp as inspection_bp
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(process_bp, url_prefix='/api')
    app.register_blueprint(inspection_bp, url_prefix='/api')

    # Health check endpoint
    @app.route('/api/health')
    def health():
        return {
            'status': 'healthy',
            'message': 'AOI Backend is running',
            'database': 'connected' if check_db_connection() else 'disconnected'
        }

    return app


def check_db_connection():
    """檢查資料庫連接"""
    try:
        from app.database import engine
        with engine.connect() as conn:
            conn.execute('SELECT 1')
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
