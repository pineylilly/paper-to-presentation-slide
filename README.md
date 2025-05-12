# Presentation Slides Generator From Academic Papers

A system that can automatically generate presentation slides from scientific papers. This is part of a final project in 2110572 Natural Language Processing Systems 2/2024 in Chulalongkorn University.

![Overview](https://github.com/user-attachments/assets/44492534-29b0-4e8d-8a0c-dcf749af2a30)

## Installation

### Prerequisites

- Docker installed on the machine.
- For Linux, please also install `screen`.
- A Node.js and Node Package Manager (npm).
- Python 3.10+ (you may use Miniconda or venv).
- Google GenAI key, which can be generated in [Google Cloud Platform](https://cloud.google.com/).

### Pulling Docker Images

This project requires [deepfigures-open](https://github.com/allenai/deepfigures-open) to extract images from paper. Therefore, the image must be pulled before running the application.

- Pull the images from Docker Hub.

```sh
docker image pull sampyash/vt_cs_6604_digital_libraries:deepfigures_cpu_0.0.6
```

- Change the image tag

```sh
docker tag sampyash/vt_cs_6604_digital_libraries:deepfigures_cpu_0.0.6 deepfigures-cpu:0.0.1
```

### Configuring and Running Backend

- From the root directory of the repository, navigate to `backend` directory.
```sh
cd backend
```

- Install Python libraries and dependencies in `requirements.txt`.
```sh
pip install -r requirements.txt
```

- Create environment variable file `.env` and fill the Google GenAI key in `GOOGLE_API_KEY`.
```env
GOOGLE_API_KEY=<fill_here>
```

- Run the backend server. For Linux (e.g. Ubuntu, Debian, ...), you can create new screen session by running `screen -S <screen_name>`.
```sh
uvicorn main:app
```

### Configuring and Running Frontend

- From the root directory of the repository, navigate to `frontend` directory.
```sh
cd frontend
```

- Install node modules.
```sh
npm install
```

- Build the project.
```sh
npm run build
```

- Start the server. Like the backend, for Linux, you can create new screen session by running `screen -S <screen_name>`.
```sh
npm run start
```

**Note:** You can set the port of the frontend server by appending `-p <port_number>` in the `start` argument in `package.json`

**Note 2:** For Linux users who set the port below 1024, please install `libcap2-bin` and configure as shown below:
```sh
sudo apt-get install libcap2-bin
sudo setcap cap_net_bind_service=+ep `readlink -f \`which node\`` 
```
