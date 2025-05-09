# Install fnm and Node.js
sudo apt-get install unzip

curl -o- https://fnm.vercel.app/install | bash
source /home/ubuntu/.bashrc
fnm install 22

# Install Slidev
npm install -g @slidev/cli playwright-chromium @slidev/theme-default

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install the Docker packages
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Docker image
sudo docker image pull sampyash/vt_cs_6604_digital_libraries:deepfigures_cpu_0.0.6

# Set permission
sudo groupadd docker
sudo usermod -aG docker ubuntu

# Change name of docker image
sudo docker tag sampyash/vt_cs_6604_digital_libraries:deepfigures_cpu_0.0.6 deepfigures-cpu:0.0.1

# Install Miniconda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh

source ~/miniconda3/bin/activate

conda init --all

conda activate

# Allow port 80 when start Next.js server
sudo apt-get install libcap2-bin
sudo setcap cap_net_bind_service=+ep `readlink -f \`which node\`` 
