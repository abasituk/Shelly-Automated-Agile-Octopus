#!/bin/bash

GITHUB_REPO_URL="https://github.com/abasituk/Shelly-Automated-Agile-Octopus"

HOME_DIRECTORY=$(eval echo ~${SUDO_USER}) # Find the home directory so the install works for different usernames
INSTALL_DIRECTORY="${HOME_DIRECTORY}/shelly"

SERVICE_FILES="shellycontrol.service webgraph.service"


echo "Installing the Shelly-Automated-Agile-Octopus system from https://github.com/abasituk/Shelly-Automated-Agile-Octopus"

# Make sure the installation is ran with sudo to allow the systemd services to be installed
if [ "$EUID" -ne 0 ]; then
    echo "Please run this installation script with sudo:"
    echo " sudo ./install.sh"
    exit 1
fi


# Update the package list and install the needed packages initially: git and python3-venv
echo "Updating package list and installing git and python3-venv"
apt update
apt install -y git python3-venv


# Make an installation directory if it doesn't exist
echo "Creating an installation directory: ${INSTALL_DIRECTORY}"
mkdir -p "${INSTALL_DIRECTORY}"


# Give the user ownership of the directory to allow editing without sudo
chown -R ${SUDO_USER}:${SUDO_USER} "${INSTALL_DIRECTORY}"


# Clone the repo into a temporary directory
echo "Cloning the repository from ${GITHUB_REPO_URL} to ${TEMP_CLONE_DIRECTORY}"
TEMP_CLONE_DIRECTORY="/tmp/shelly_clone_$(date +%s)"
sudo -u ${SUDO_USER} git clone "${GITHUB_REPO_URL}" "${TEMP_CLONE_DIRECTORY}"


# Move everything from the temporary directory to the installation directory
echo "Moving the cloned files to ${INSTALL_DIRECTORY}"
sudo -u ${SUDO_USER} mv "${TEMP_CLONE_DIRECTORY}"/* "${INSTALL_DIRECTORY}/"
sudo -u ${SUDO_USER} mv "${TEMP_CLONE_DIRECTORY}"/.* "${INSTALL_DIRECTORY}/" 2>/dev/null

# Remove the temporary directory
echo "Removing the temporary directory ${TEMP_CLONE_DIRECTORY}"
rm -rf "${TEMP_CLONE_DIRECTORY}"


# Move to the installation directory or send an error msg if it fails
cd "${INSTALL_DIRECTORY}" || { echo "Failed to change directory to ${INSTALL_DIRECTORY}. Exiting."; exit 1; }


# Set up the venv
echo "Setting up Python virtual environment in ${INSTALL_DIRECTORY}"
sudo -u ${SUDO_USER} python3 -m venv "${INSTALL_DIRECTORY}"


# Activate the venv and install the dependencies
echo "Activating the virtual environment and installing Python dependencies from requirements.txt"
sudo -u ${SUDO_USER} /bin/bash -c "source ${INSTALL_DIRECTORY}/bin/activate && pip install -r requirements.txt"


# Set up systemd services
echo "Setting up the systemd services so the system runs on boot"
SYSTEMD_SOURCE_DIR="${INSTALL_DIRECTORY}/services"

for service_file in ${SERVICE_FILES}; do
    SOURCE_PATH="${SYSTEMD_SOURCE_DIR}/${service_file}"
    DESTINATION_PATH="/etc/systemd/system/${service_file}"

    if [ -f "${SOURCE_PATH}" ]; then
        echo "Copying ${SOURCE_PATH} to ${DESTINATION_PATH}"
        cp "${SOURCE_PATH}" "${DESTINATION_PATH}"

    else
        echo ""
        echo "Warning: The service file ${service_file} could not be found at ${SOURCE_PATH} and will be skipped =================="
        echo ""
    fi
done


# Reload systemd manager configuration to recognize new service files
echo "Reloading systemd daemon"
systemctl daemon-reload


# Enable and Start Services
echo "Enabling and starting services"
for service_file in ${SERVICE_FILES}; do
    SERVICE_NAME=$(basename "${service_file}") # Get just the filename (e.g., shellycontrol.service)
     if [ -f "/etc/systemd/system/${SERVICE_NAME}" ]; then
        echo "Enabling ${SERVICE_NAME}"
        systemctl enable "${SERVICE_NAME}"

        echo "Starting ${SERVICE_NAME}"
        systemctl start "${SERVICE_NAME}"
    else
        echo "Skipping enabling and starting the service: ${SERVICE_NAME} as the file could not be copied successfully."
    fi
done

# Write next steps
echo ""
echo "Finished installation ================================================================="
echo ""
echo "Next steps you need to take:"
echo "1) Navigate to your installation directory using:"
echo "     cd ${INSTALL_DIRECTORY}"
echo ""

echo "2) Open your config.ini and add your Shelly and Tariff Details using:"
echo "     nano config.ini"
echo "   You will need your device ID, server URI and Authorization token."
echo ""


echo "3) If you would like to use a screen for your Pi, you may have to enable i2c to connect to it"
echo "   please note these steps or see https://github.com/abasituk/Shelly-Automated-Agile-Octopus for a visual guide:"
echo "   run the command:"
echo "     sudo raspi-config"
echo "   Select '3 Interface Options'"
echo "   Select the option saying 'I2C'"
echo "   Select Yes to enable I2C"
echo "   Once it's enabled, finally use your right arrow to select 'Finish'"
echo ""


echo "4) After adding your details to the config.ini and enabling I2C, you can reload -"
echo "   your services so the system will start upon booting your Pi using:"
echo "     sudo systemctl restart shellycontrol.service webgraph.service"
echo ""

echo ""
echo "Your Shelly details are available at https://control.shelly.cloud/"
echo "For a visual guide on finding your Shelly details, please see https://github.com/abasituk/Shelly-Automated-Agile-Octopus"
echo ""
