# NAG DSP-10
audio processor


rel v1.0 --------------------------------
скорость i2c - 400k: sudo fdtput -t i /boot/sun50i-h5-nanopi-neo-plus2.dtb /soc/i2c@01c2ac00 clock-frequency 400000

загрузчик шьет DSP по i2c из dsp-10.xml

MuteOff(MP8), DACinit(0x87) - по завершении загрузки 
