{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  name = "cents-python";
  nativeBuildInputs = with pkgs.buildPackages; [
    python312 
    poetry 
    libmysqlclient 
    pkg-config 
    mariadb
  ];

  shellHook = ''

    DJANGO_ENV=test
    EMAIL=internal
    DOMAIN=localhost
    DEBUG=True
    DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"
    CSRF_TRUSTED_ORIGINS="http://localhost https://localhost"

    MYSQL_BASEDIR=${pkgs.mariadb}
    MYSQL_HOME="$PWD/mysql"
    MYSQL_DATADIR="$MYSQL_HOME/data"
    export MYSQL_UNIX_PORT="$MYSQL_HOME/mysql.sock"
    MYSQL_PID_FILE="$MYSQL_HOME/mysql.pid"
    alias mysql='mysql -u root'

    if [ ! -d "$MYSQL_HOME" ]; then
      # Make sure to use normal authentication method otherwise we can only
      # connect with unix account. But users do not actually exists in nix.
      mysql_install_db --no-defaults --auth-root-authentication-method=normal \
        --datadir="$MYSQL_DATADIR" --basedir="$MYSQL_BASEDIR" \
        --pid-file="$MYSQL_PID_FILE"
    fi

    # Starts the daemon
    # - Don't load mariadb global defaults in /etc with `--no-defaults`
    # - Disable networking with `--skip-networking` and only use the socket so 
    #   multiple instances can run at once
    mysqld --no-defaults --skip-networking --datadir="$MYSQL_DATADIR" --pid-file="$MYSQL_PID_FILE" \
      --socket="$MYSQL_UNIX_PORT" 2> "$MYSQL_HOME/mysql.log" &
    MYSQL_PID=$!

    finish()
    {
      mysqladmin -u root --socket="$MYSQL_UNIX_PORT" shutdown
      kill $MYSQL_PID
      wait $MYSQL_PID
    }
    trap finish EXIT

    poetry install

    mysql -uroot -e "CREATE DATABASE IF NOT EXISTS finances;"
  '';
}