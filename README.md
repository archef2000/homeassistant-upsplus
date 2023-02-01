[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# Home Assistant custom integration

This custom integration is for the [UPS](https://wiki.52pi.com/index.php/EP-0136) from 52PI.

It communicates over I2C this needs to be enabled beforehand
## Home Assistannt OS
Use the ssh addon to edit the ˋ/boot/config.txtˋ file and add ˋdtparam=i2c_arm=onˋ
## Home Assistant Supervised
Run ˋsudo raspi-configˋ -> ˋInterface Optionsˋ -> ˋI2Cˋ -> ˋEnableˋ and then reboot
## Home Assistant Core
Follow the same procedure as with the supervised version but make sure to mount /dev/i2c-1 in the container after reboot
