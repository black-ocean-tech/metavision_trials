# Build install driver, SDK, plugin and exec samples.

## Build
- Basically, follow the instructions as written in https://github.com/prophesee-ai/openeb.
- Install Ubuntu 24.04.1 LTS in your system.
- Clone repo.
```
cd ~
mkdir git
cd git
git clone -b 5.0.0 https://github.com/prophesee-ai/openeb.git
```
- Install required apt packs.
```
sudo apt update
sudo apt -y install apt-utils build-essential software-properties-common wget unzip curl git cmake
sudo apt -y install libopencv-dev libboost-all-dev libusb-1.0-0-dev libprotobuf-dev protobuf-compiler
sudo apt -y install libhdf5-dev hdf5-tools libglew-dev libglfw3-dev libcanberra-gtk-module ffmpeg
```
- Install miniforge.
  - 途中訊かれることはデフォルトで良い。
```
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```
- Reboot.
- Install pybind.
```
wget https://github.com/pybind/pybind11/archive/v2.11.0.zip
unzip v2.11.0.zip
cd pybind11-2.11.0/
mkdir build && cd build
cmake .. -DPYBIND11_TEST=OFF
cmake --build .
sudo cmake --build . --target install
```
- Build, install SDK.
  - しばらくかかる。
```
cd ~
cd git/openeb
mkdir build
cd build
cmake .. -DBUILD_TESTING=OFF
cmake --build . --config Release -- -j 4
sudo cmake --build . --target install
```
- Edit ~/.bashrc, add following lines.
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
export HDF5_PLUGIN_PATH=$HDF5_PLUGIN_PATH:/usr/local/hdf5/lib/plugin  # On Ubuntu 22.04
export HDF5_PLUGIN_PATH=$HDF5_PLUGIN_PATH:/usr/local/lib/hdf5/plugin  # On Ubuntu 24.04
```
- Reboot.
- Install OpenCV for trials.
  - conda-forgeからOpenCVがインストールされる。
```
(base) $ conda install opencv
```

## Add plugin
- Basically, follow the instructions as written in https://centuryarks.com/wp-content/uploads/2023/08/SilkyEvCamHD_Software_SettingGuide_JP_20230518a.pdf.
- Download, extract, install plugin.
```
cd ~
wget https://centuryarks.com/wp-content/uploads/2024/10/SilkyEvCam_Plugin_Installer_for_ubuntu_v5.0.0.zip
unzip SilkyEvCam_Plugin_Installer_for_ubuntu_v5.0.0.zip
cd SilkyEvCam_Plugin_Installer_for_ubuntu_v5.0.0/SilkyEvCam_Plugin_Installer_for_ubuntu_v5.0.0
./CA_Silky_installer.sh
```
- Reboot.

## Exec samples.
- Liveview.
```
cd ~
cd git/openeb/sdk/modules/stream/python/samples/metavision_camera_stream_slicer
python metavision_camera_stream_slicer.py
```
  - ![_](liveview_sample.png)