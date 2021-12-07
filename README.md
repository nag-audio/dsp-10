# NAG DSP-10
audio processor

---------------------Downloader_32.exe-----------------------------

Automatic load dsp project files from DSP10.
0. Install "SigmaStudio 4.6" on your PC (NOT need make run after install)
1. Connect DSP to LAN Router wint active DHCP server by Wire and check dynamic IP address from PC
2. Run "downloader_32.exe" (WIN10/64 was tested)
3. Program will find DSP10 in local network and download files to:  "C:\NAG\DSP-10"
4. Automaticly open dsp-10.dspproj in SigmaStudio 

-Attention! now you need change IP address in Sigma project (default: 192.168.1.170 port: 8086), then:
open Hardware configuration tab ---> Right mouse button on TCPIP box ---> Show TCPIP settings --> enter current IP address (check it in dhcp server)

After change parametrs in block schematic you need make uploading to DSP
1.  press "SAVE" button (Ctrl+S)
2.  press "Link Compile Connect" button for build new schematic with all modifications (vol, filters, delays and etc.) (check warnings and errors!)
3.  press "Export System Files" button for export files to DSP, SigmaStudio automaticly upload files to DSP.
4.  If all ok (status "Active: Downloaded") now you can change volume or filter frequency or delay or mute or EQ parameters.
---------------------------------------------------------------------
