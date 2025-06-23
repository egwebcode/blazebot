#!/data/data/com.termux/files/usr/bin/bash

echo "Atualizando pacotes..."
pkg update -y && pkg upgrade -y

echo "Instalando dependências..."
pkg install apache2 php mariadb git nano unzip -y

echo "Parando Apache e MariaDB se estiverem rodando..."
pkill apache2
pkill mysqld

echo "Clonando DVWA..."
cd /data/data/com.termux/files/usr/share/apache2/default-site/htdocs/ || exit
if [ -d DVWA ]; then
  echo "Pasta DVWA já existe, removendo..."
  rm -rf DVWA
fi
git clone https://github.com/digininja/DVWA.git

echo "Configurando DVWA..."
cd DVWA/config || exit
cp config.inc.php.dist config.inc.php

sed -i "s/\$_DVWA'db_user' *= *getenv('DB_USER') ?:.*/\1'dvwa';/" config.inc.php
sed -i "s/\$_DVWA'db_password' *= *getenv('DB_PASSWORD') ?:.*/\1'dvwapass';/" config.inc.php
sed -i "s/\$_DVWA'db_server' *= *getenv('DB_SERVER') ?:.*/\1'127.0.0.1';/" config.inc.php
sed -i "s/\$_DVWA'db_database' *= *getenv('DB_DATABASE') ?:.*/\1'dvwa';/" config.inc.php

echo "Iniciando MariaDB..."
mysqld_safe &

sleep 5

echo "Criando banco e usuário MariaDB para DVWA..."
mariadb -u root <<EOF
CREATE DATABASE IF NOT EXISTS dvwa;
CREATE USER IF NOT EXISTS 'dvwa'@'localhost' IDENTIFIED BY 'dvwapass';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

echo "Iniciando Apache..."
apachectl start

echo "Instalação e configuração concluída!"
echo "Abra no navegador: http://localhost:8080/DVWA/setup.php"
echo "Clique em 'Create / Reset Database' e depois acesse http://localhost:8080/DVWA/login.php"
echo "Login padrão: admin / password"
