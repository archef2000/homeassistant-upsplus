# 52PI UPS Integration

## Enable I2C
### Home Assistannt OS
Use the ssh addon to edit the `/boot/config.txt` file and add `dtparam=i2c_arm=on` and `dtparam=i2c_vc=on`
### Home Assistant Supervised
Run `sudo raspi-config` -> `Interface Options` -> `I2C` -> `Enable` and then reboot
### Home Assistant Core
Follow the same procedure as with the supervised version but make sure to mount `/dev/i2c-1` in the container after reboot


## Updating the UPS
### Checklist
1. Entered UPS OTA mode via `Enter OTA` button from integration
2. Shutdown system
3. Cut external power
4. Remove/Reinsert batteries
5. Connect external power
6. Start system
7. Call `upsplus.update` service and wail until the response is successful
8. Shutdwn system
9. Remove/Reinsert batteries
10. Start system
