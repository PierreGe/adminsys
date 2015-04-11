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
    docker pull $app
    docker run -d $app
  fi
  # add wordpress
  #if [[ $POST =~ ^wordpressName=(.*)\&wordpressPort=(.*)\&mysqlPass=(.*)$ ]]; then
   # wpName="${BASH_REMATCH[1]}"
    #wpPort="${BASH_REMATCH[2]}"
    #mysqlPass="${BASH_REMATCH[3]}"
    #docker run --name mysql -e MYSQL_ROOT_PASSWORD=$mysqlPass -d mysql:latest > /dev/null
    #docker run --name "mysql-"$wpName -e MYSQL_ROOT_PASSWORD=$mysqlPass -d mysql:latest --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
    #docker run --name $wpName --link "mysql-"$wpName:"mysql-"$wpName -p $wpPort:80 -d wordpress -e WORDPRESS_DB_USER="root" -e WORDPRESS_DB_PASSWORD="$mysqlPass"
#  fi
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
#echo '        <input type="checkbox" name="wordpress" value="install" id="wordpress">'
#echo '        <label for="wordpress"><img src="https://s.w.org/favicon.ico" width="15" height="15">Wordpress</label>'
#echo '        <div class="installerMenu" id="wordpressInstaller">'
#echo '        <label>Nom du container</label>'  
#echo '        <input type="text" name="wordpressName" value="wordpress" >'
#echo '        <label>Port</label>'
#echo '        <input type="text" name="wordpressPort" value="8080" >'
#echo '        <label>Mot de passe mysql</label>'
#echo '        <input type="password" name="mysqlPass" value="root" >'
#echo '        </div>'
#echo '        <input type="text" name="test" value="test">'
#echo '        <input type="submit" value="Create" style="display:block; margin:20 0 0 10px;">'
echo '         <input type="button" onclick="this.form.submit();" value="Delete">'
echo '      </form>'
echo '    </div>'


echo '    <div class="installer" id="dockerhubInstaller">'
echo '      <form method="post" action="docker-handler.cgi">'
echo '         Docker name (from DockerHub): <input type="text" name="installDockerhubApp"><br>'
echo '      <input type="submit"value="Create" style="display:block; margin:20 0 0 10px;">'
echo '      </form>'
echo '    </div>'

echo '  </div>'
echo '</body>'
echo '</html>'

exit 0
