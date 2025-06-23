#!/data/data/com.termux/files/usr/bin/bash

echo "=== [1/9] Atualizando Termux..."
pkg update -y && pkg upgrade -y

echo "=== [2/9] Instalando pacotes necessários..."
pkg install apache2 php php-mysqli php-gd mariadb git curl unzip nano -y

echo "=== [3/9] Matando Apache e MariaDB..."
pkill apache2
pkill mariadbd

echo "=== [4/9] Preparando ambiente MariaDB..."
mkdir -p $PREFIX/var/run/mysqld
mkdir -p $PREFIX/var/lib/mysql

echo "=== [5/9] Clonando DVWA para Apache..."
cd /data/data/com.termux/files/usr/share/apache2/default-site/htdocs/ || exit
rm -rf DVWA
git clone https://github.com/digininja/DVWA.git
cd DVWA/config
cp config.inc.php.dist config.inc.php

echo "=== [6/9] Corrigindo config.inc.php..."
sed -i "s/\$_DVWA'db_user'.*/\$_DVWA[ 'db_user' ] = 'dvwa';/" config.inc.php
sed -i "s/\$_DVWA'db_password'.*/\$_DVWA[ 'db_password' ] = 'dvwapass';/" config.inc.php
sed -i "s/\$_DVWA'db_server'.*/\$_DVWA[ 'db_server' ] = 'localhost';/" config.inc.php
sed -i "s/\$_DVWA'db_database'.*/\$_DVWA[ 'db_database' ] = 'dvwa';/" config.inc.php
sed -i "s/\$_DVWA'default_security_level'.*/\$_DVWA[ 'default_security_level' ] = 'low';/" config.inc.php

echo "=== [7/9] Iniciando MariaDB..."
mariadb-install-db --user=root --datadir=$PREFIX/var/lib/mysql
mariadbd-safe --datadir=$PREFIX/var/lib/mysql --socket=$PREFIX/var/run/mysqld/mysqld.sock &
sleep 8

echo "=== [8/9] Criando banco e usuário DVWA..."
mariadb --socket=$PREFIX/var/run/mysqld/mysqld.sock <<EOF
CREATE DATABASE IF NOT EXISTS dvwa;
CREATE USER IF NOT EXISTS 'dvwa'@'localhost' IDENTIFIED BY 'dvwapass';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "=== [9/9] Iniciando Apache..."
apachectl start
sleep 2

echo "=== [AUTO] Criando banco DVWA via setup.php..."
curl -s http://localhost:8080/DVWA/setup.php | grep -q 'Database has been created' && echo "✔️ Banco criado com sucesso!" || echo "⚠️ Verifique setup.php manualmente se necessário."

echo
echo "===================================================="
echo "✅ INSTALAÇÃO COMPLETA DO DVWA!"
echo "Acesse no navegador: http://localhost:8080/DVWA/login.php"
echo "Login padrão: admin"
echo "Senha padrão: password"
echo "===================================================="
