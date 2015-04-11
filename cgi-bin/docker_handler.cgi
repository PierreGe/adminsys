#!/bin/bash

if [ "$REQUEST_METHOD" = "POST" ]; then
  POST=$(</dev/stdin)
  # Start / Stop container
  if [[ $POST =~ ^toggleService=(.*)$ ]]; then
    service="${BASH_REMATCH[1]}"
    if [[ "$(docker ps)" =~ $service ]]; then
      docker stop $service > /dev/null
    else
      docker start $service > /dev/null
    fi
  fi
  if [[ $POST =~ ^duplicate=(.*)$ ]]; then
    service="${BASH_REMATCH[1]}"
    if [[ "$(docker ps)" =~ $service ]]; then
      stopped=true
      docker stop $service > /dev/null
    fi
    docker commit $service $service-duplicated
    docker run -d $service-duplicated
    if [ "$stopped" = true ] ; then
      docker start $service
    fi
  fi
  if [[ $POST =~ ^delete=(.*)$ ]]; then
    service="${BASH_REMATCH[1]}"
    if [[ "$(docker ps)" =~ $service ]]; then
      docker stop $service > /dev/null
    fi
    docker rm $service
  fi
  # Rename container
  if [[ $POST =~ ^newName=(.*)\&oldName=(.*)$ ]]; then
    newName="${BASH_REMATCH[1]}"
    oldName="${BASH_REMATCH[2]}"
    docker rename "$oldName" "$newName"
  fi
  if [[ $POST =~ ^installDockerhubApp=(.*)$ ]]; then
    app="${BASH_REMATCH[1]}"
    (docker pull $app > /dev/null; docker run -d $app > /dev/null )&
  fi
  # add wordpress
  if [[ $POST =~ ^wordpress=install\&wordpressName=(.*)\&wordpressPort=(.*)\&mysqlPass=(.*)$ ]]; then
    wpName="${BASH_REMATCH[1]}"
    mysqlName="mysql-"$wpName
    wpPort="${BASH_REMATCH[2]}"
    mysqlPass="${BASH_REMATCH[3]}"
    docker run --name $mysqlName -e MYSQL_ROOT_PASSWORD=$mysqlPass -d mysql:latest > /dev/null
    docker run --name $wpName --link $mysqlName:mysql -p $wpPort:80 -d wordpress > /dev/null
    #docker run --name "mysql-"$wpName -e MYSQL_ROOT_PASSWORD=$mysqlPass -d mysql:latest --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
  fi
fi

echo "Content-type: text/html"
echo ""

echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>Adminsys</title>'
echo '<link rel="stylesheet" type="text/css" href="../style/style.css">'
echo '<link rel="stylesheet" type="text/css" href="../style/togglebutton.css">'
echo '</head>'
echo '<body>'
echo '  <div id="header">'
echo '  </div>'
echo '  <div id="content">'
echo '    <div id="userinfo">'
echo '      <p>Nom : root</p>'
echo '      <p>Pass : root</p>'
echo '    </div>'
echo '    <div id="services">'
python ../format/containers.py "$(docker ps -a)"
echo '      <div id="tools">'
echo '        <input type="button" onclick="location.replace(location.href)" value="Reload" id="reloadButton">'
echo '      </div>'
echo '    </div>'

echo '    <div class="installer" id="customInstaller">'
echo '      <form method="post" action="docker_handler.cgi">'
echo '        <input type="checkbox" name="wordpress" value="install" id="wordpress">'
echo '        <label for="wordpress"><img src="https://s.w.org/favicon.ico" width="15" height="15">Wordpress</label>'
echo '        <div class="installerMenu" id="wordpressInstaller">'
echo '          <table>'
echo '            <tr>'
echo '              <td><label>Nom du container</label></td>'
echo '              <td><input type="text" name="wordpressName" value="wordpress" ><td>'
echo '            </tr>'
echo '            <tr>'
echo '              <td><label>Port</label></td>'
echo '              <td><input type="text" name="wordpressPort" value="8080" ></td>'
echo '            </tr>'
echo '            <tr>'
echo '              <td><label>Mot de passe mysql</label></td>'
echo '              <td><input type="password" name="mysqlPass" value="root" ></td>'
echo '            </tr>'
echo '          </table>'
echo '        </div>'
echo '        <input type="button" onclick="this.form.submit();" value="Create" style="display:block; margin:20 0 0 10px;">'
echo '      </form>'
echo '    </div>'


echo '    <div class="installer" id="dockerhubInstaller">'
echo '      <form method="post" action="docker_handler.cgi">'
echo '         Docker name (from DockerHub): <input type="text" name="installDockerhubApp"><br>'
echo '      <input type="submit"value="Create" style="display:block; margin:20 0 0 10px;">'
echo '      </form>'
echo '    </div>'

echo '  </div>'
echo '</body>'
echo '</html>'

exit 0
