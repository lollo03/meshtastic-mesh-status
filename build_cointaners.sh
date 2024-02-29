rm -rf meshtastic-mesh-status/
git clone https://github.com/lollo03/meshtastic-mesh-status.git
sudo docker build meshtastic-mesh-status/bot/ -t lolloandr/meshtastic-status-bot
sudo docker build meshtastic-mesh-status/databaser/ -t lolloandr/meshtastic-status-databaser

