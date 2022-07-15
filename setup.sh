#!/bin/bash

DNF_LOC=/etc/dnf/dnf.conf
LIGHTDM_LOC=/etc/lightdm/

echo "Starting Setup";
echo "Downloading config files";
sudo dnf install git;
cp Qtile-config/Pictures/Wallpaper ~/Pictures/Wallpaper/
git clone https://github.com/MeetMaratha/Qtile-config.git;
echo "Making DNF Quicker";
echo "fastestmirror=true" >> $DNF_LOC;
echo "max_parallel_downloads=10" >> $DNF_LOC;
echo "defaultyes=True" >> $DNF_LOC;
echo "Enabling RPM Fusion repos";
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
echo "Installing Xorg"
sudo dnf install xorg-x11-server-Xorg xorg-x11-xinit network-manager-applet xorg-x11-drv-libinput mesa-dri-drivers pulseaudio gvfs lightdm-gtk NetworkManager-wifi; 
echo "Setting Lightdm"
systemctl enable lightdm; 
systemctl set-default graphical.target;
sudo cp Qtile-config/etc/lightdm/* $LIGHTDM_LOC
echo "Installing Plugins for media"
sudo dnf install gstreamer1-plugins-{bad-\*,good-\*,base} gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel
sudo dnf install lame\* --exclude=lame-devel
sudo dnf group upgrade --with-optional Multimedia
echo "Adding Roboto Fonts and softwares"
sudo dnf copr enable dani/qgis;
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc;
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf check-update
sudo dnf install google-roboto-condensed-fonts google-roboto-fonts google-roboto-mono-font alacritty firefox pcmanfm htop lxappearance transmission python qalculate gimp nitrogen gparted lutris steam bleachbit leafpad evince libinput xdotool ristretto flameshot timeshift vlc picom libreoffice qgis python3-qgis qgis-grass texlive-scheme-full texstudio code audacious xarchiver
echo "Enabling Flatpak"
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
echo "Installing Flatpaks"
read -p "Do you wanna install Joplin? (y/N)" ans
if [ $(ans) == 'y' || $(ans) == 'Y']; then
    flatpak install flathub net.cozic.joplin_desktop
elif [ $(ans) == 'y' || $(ans) == 'Y']; then
    echo "Not Installed Joplin"
else
    flatpak install flathub net.cozic.joplin_desktop
fi
read -p "Do you wanna install Github Desktop? (y/N)" ans
if [ $(ans) == 'y' || $(ans) == 'Y']; then
    flatpak install flathub io.github.shiftey.Desktop
elif [ $(ans) == 'y' || $(ans) == 'Y']; then
    echo "Not Installed Github Desktop"
else
    flatpak install flathub io.github.shiftey.Desktop
fi
read -p "Do you wanna install Telegram Desktop? (y/N)" ans
if [ $(ans) == 'y' || $(ans) == 'Y']; then
    flatpak install flathub org.telegram.desktop
elif [ $(ans) == 'y' || $(ans) == 'Y']; then
    echo "Not Installed Telegram Desktop"
else
    flatpak install flathub org.telegram.desktop
fi
echo "Moving Config files"
cp -r Qtile-config/config/* .config/
cp -r Qtile-config/icons/* .icons/
cp -r Qtile-config/themes/* .themes/
cp -r Qtile-config/home/* .
cp -r Qtile-config/local/share/fonts/* .local/share/fonts/
sudo cp -r Qtile-config/etc/X11/xorg.conf.d/* /etc/X11/xorg.conf.d/
echo "Install pip modules"
pip install numpy pandas matplotlib