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
      docker stop $service > /dev/null
    fi
    docker commit $service $service-duplicated
  fi
  # Rename container
  if [[ $POST =~ ^newName=(.*)\&oldName=(.*)$ ]]; then
    newName="${BASH_REMATCH[1]}"
    oldName="${BASH_REMATCH[2]}"
    docker rename "$oldName" "$newName"
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
echo '    <div id="installer">'
echo '      <form method="post" action="docker-handler.cgi">'
echo '        <input type="checkbox" value="Wordpress" id="wordpress">'
echo '        <label for="wordpress"><img src="https://s.w.org/favicon.ico" width="15" height="15">Wordpress</label>'
echo '        <div class="installerMenu" id="wordpressInstaller">'
echo '          some stuff here to config'
echo '        </div>'
echo '        <input type="button" value="Créer les services" style="display:block; margin:20 0 0 10px;">'
echo '      </form>'
echo '    </div>'
echo '  </div>'
echo '</body>'
echo '</html>'

exit 0
