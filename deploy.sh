#!/bin/bash
# Deployment script for Portal Saúde on Ubuntu/Debian server
# Usage: ./deploy.sh [environment]
# Environment: production (default) or staging

set -e

ENVIRONMENT=${1:-production}
PROJECT_NAME="portal-saude"
PROJECT_DIR="/opt/$PROJECT_NAME"
VENV_DIR="$PROJECT_DIR/venv"
USER="www-data"
GROUP="www-data"

echo "🚀 Deploying Portal Saúde ($ENVIRONMENT)..."

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    nginx \
    curl \
    git \
    supervisor

# Create project directory
echo "📁 Creating project directory..."
mkdir -p $PROJECT_DIR
chown -R $USER:$GROUP $PROJECT_DIR

# Clone or update repository
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "🔄 Updating repository..."
    cd $PROJECT_DIR
    sudo -u $USER git pull
else
    echo "📥 Cloning repository..."
    # Replace with your repository URL
    sudo -u $USER git clone https://github.com/yourusername/portal-saude.git $PROJECT_DIR
fi

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    sudo -u $USER python3 -m venv $VENV_DIR
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
sudo -u $USER $VENV_DIR/bin/pip install --upgrade pip
sudo -u $USER $VENV_DIR/bin/pip install -r $PROJECT_DIR/requirements-prod.txt

# Configure environment variables
echo "🔧 Configuring environment..."
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp $PROJECT_DIR/.env.example $PROJECT_DIR/.env
    echo "⚠️  Please edit $PROJECT_DIR/.env with your production settings"
    echo "   SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS, etc."
    exit 1
fi

# Setup PostgreSQL database
echo "🗄️  Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE ${PROJECT_NAME}_${ENVIRONMENT};" || true
sudo -u postgres psql -c "CREATE USER ${PROJECT_NAME}_user WITH PASSWORD '${PROJECT_NAME}_password';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${PROJECT_NAME}_${ENVIRONMENT} TO ${PROJECT_NAME}_user;" || true

# Run Django management commands
echo "🔄 Running Django migrations..."
cd $PROJECT_DIR
sudo -u $USER $VENV_DIR/bin/python sistema/manage.py migrate --noinput
sudo -u $USER $VENV_DIR/bin/python sistema/manage.py collectstatic --noinput
sudo -u $USER $VENV_DIR/bin/python sistema/manage.py compress --force

# Configure Gunicorn
echo "🦄 Configuring Gunicorn..."
cat > /etc/systemd/system/$PROJECT_NAME.service << EOF
[Unit]
Description=Portal Saúde Gunicorn Daemon ($ENVIRONMENT)
After=network.target postgresql.service

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$PROJECT_DIR/sistema
Environment="PATH=$VENV_DIR/bin"
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$VENV_DIR/bin/gunicorn sistema.wsgi:application \
    --bind unix:/run/$PROJECT_NAME.sock \
    --workers 3 \
    --timeout 120 \
    --log-level info \
    --access-logfile /var/log/$PROJECT_NAME/access.log \
    --error-logfile /var/log/$PROJECT_NAME/error.log

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/$PROJECT_NAME << EOF
server {
    listen 80;
    server_name _;

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $PROJECT_DIR/imagens_exames/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://unix:/run/$PROJECT_NAME.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 75s;
        proxy_send_timeout 3600s;
        proxy_read_timeout 3600s;
    }
}
EOF

# Create log directory
mkdir -p /var/log/$PROJECT_NAME
chown -R $USER:$GROUP /var/log/$PROJECT_NAME

# Enable and start services
echo "⚡ Enabling and starting services..."
ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

systemctl daemon-reload
systemctl enable $PROJECT_NAME.service
systemctl restart $PROJECT_NAME.service
systemctl restart nginx

echo "✅ Deployment completed successfully!"
echo "🌍 Access your application at: http://$(curl -s ifconfig.me)"
echo "📝 Logs: /var/log/$PROJECT_NAME/"
echo "🛠️  Management: systemctl status $PROJECT_NAME.service"