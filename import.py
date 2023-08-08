import subprocess

# Step 1: Install dependencies
install_command = "pip install Flask Pillow requests transformers torch torchvision torchaudio"
subprocess.run(install_command, shell=True)

# Step 2: Clone the repository using git protocol
repo_url = "git@github.com:ludwig7685/image-caption-generation-with-ai-and-api.git"
clone_command = f"git clone {repo_url}"
subprocess.run(clone_command, shell=True)

# Step 3: Change directory to the cloned repository
repo_name = repo_url.split("/")[-1].split(".git")[0]
subprocess.run(f"cd {repo_name}", shell=True)

# Step 4: Run app.py from the image-caption-generation-with-ai-and-api folder
run_command = "python app.py"
subprocess.run(run_command, shell=True)
