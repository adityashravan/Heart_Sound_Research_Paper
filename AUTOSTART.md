# Auto-Start Configuration for Raspberry Pi

## Option 1: Desktop Auto-start (Recommended for GUI)

1. Create autostart directory if it doesn't exist:
```bash
mkdir -p ~/.config/autostart
```

2. Create desktop entry:
```bash
nano ~/.config/autostart/heart-classifier.desktop
```

3. Add the following content:
```ini
[Desktop Entry]
Type=Application
Name=Heart Sound Classifier
Exec=/home/admin/Frontend_RP/launch.sh
Terminal=false
StartupNotify=false
```

4. Make scripts executable:
```bash
chmod +x ~/Frontend_RP/launch.sh
chmod +x ~/Frontend_RP/heart_sound_classifier.py
```

5. Reboot to test:
```bash
sudo reboot
```

## Option 2: systemd Service (Runs in background)

1. Create service file:
```bash
sudo nano /etc/systemd/system/heart-classifier.service
```

2. Add content:
```ini
[Unit]
Description=Heart Sound Classifier GUI
After=graphical.target

[Service]
Type=simple
User=admin
Environment=DISPLAY=:0
WorkingDirectory=/home/admin/Frontend_RP
ExecStart=/usr/bin/python3 /home/admin/Frontend_RP/heart_sound_classifier.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=graphical.target
```

3. Enable and start:
```bash
sudo systemctl enable heart-classifier.service
sudo systemctl start heart-classifier.service
```

4. Check status:
```bash
sudo systemctl status heart-classifier.service
```

## Option 3: rc.local (Simple boot script)

1. Edit rc.local:
```bash
sudo nano /etc/rc.local
```

2. Add before `exit 0`:
```bash
su - admin -c "DISPLAY=:0 /home/admin/Frontend_RP/launch.sh &"
```

3. Make rc.local executable:
```bash
sudo chmod +x /etc/rc.local
```

## Troubleshooting Auto-start

### GUI doesn't appear:
- Check display variable: `echo $DISPLAY`
- Verify X server is running: `ps aux | grep X`
- Check logs: `journalctl -u heart-classifier.service`

### Application crashes on start:
- Test manually first: `python3 heart_sound_classifier.py`
- Check dependencies: `pip3 list`
- View logs: check `~/.xsession-errors`

### Want to disable auto-start:
```bash
# For desktop autostart:
rm ~/.config/autostart/heart-classifier.desktop

# For systemd:
sudo systemctl disable heart-classifier.service
sudo systemctl stop heart-classifier.service

# For rc.local:
sudo nano /etc/rc.local  # Remove the added line
```
