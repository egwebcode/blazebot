#!/data/data/com.termux/files/usr/bin/bash

echo "Atualizando pacotes..."
pkg update -y && pkg upgrade -y

echo "Instalando dependências necessárias..."
pkg install apache2 php mariadb git nano unzip -y

echo "Matando processos do Apache e MariaDB (se existirem)..."
pkill apache2
pkill mariadbd

echo "Clonando DVWA..."
cd /data/data/com.termux/files/usr/share/apache2/default-site/htdocs/ || exit
if [ -d DVWA ]; then
  echo "Removendo instalação antiga do DVWA..."
  rm -rf DVWA
fi
git clone https://github.com/digininja/DVWA.git

echo "Configurando DVWA..."
cd DVWA/config || exit
cp config.inc.php.dist config.inc.php

sed -i "s/\$_DVWA'db_user'.*/\$_DVWA[ 'db_user' ] = 'dvwa';/" config.inc.php
sed -i "s/\$_DVWA'db_password'.*/\$_DVWA[ 'db_password' ] = 'dvwapass';/" config.inc.php
sed -i "s/\$_DVWA'db_server'.*/\$_DVWA[ 'db_server' ] = 'localhost';/" config.inc.php
sed -i "s/\$_DVWA'db_database'.*/\$_DVWA[ 'db_database' ] = 'dvwa';/" config.inc.php

echo "Iniciando MariaDB..."
mariadbd-safe --datadir=$PREFIX/var/lib/mysql &

sleep 7

echo "Criando banco e usuário para DVWA no MariaDB..."
mariadb -u root <<EOF
CREATE DATABASE IF NOT EXISTS dvwa;
CREATE USER IF NOT EXISTS 'dvwa'@'localhost' IDENTIFIED BY 'dvwapass';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Iniciando Apache..."
apachectl start

echo "-------------------------------------------------------"
echo "INSTALAÇÃO COMPLETA!"
echo "Acesse no navegador: http://localhost:8080/DVWA/setup.php"
echo "Clique em 'Create / Reset Database' para criar o banco."
echo "Depois acesse http://localhost:8080/DVWA/login.php"
echo "Login padrão:"
echo "Usuário: admin"
echo "Senha: password"
echo "-------------------------------------------------------"
