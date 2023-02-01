# 52PI UPS Integration

## Enable I2C
### Home Assistannt OS
Use the ssh addon to edit the ˋ/boot/config.txtˋ file and add ˋdtparam=i2c_arm=onˋ and ˋdtparam=i2c_vc=onˋ
### Home Assistant Supervised
Run ˋsudo raspi-configˋ -> ˋInterface Optionsˋ -> ˋI2Cˋ -> ˋEnableˋ and then reboot
### Home Assistant Core
Follow the same procedure as with the supervised version but make sure to mount /dev/i2c-1 in the container after reboot
