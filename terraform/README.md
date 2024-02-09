# Terraform Deployment Guide

This guide provides instructions on how to create a Terraform virtual machine (VM) on Microsoft Azure.

## Prerequisites

Before you begin, ensure you have the following:

- [Terraform](https://www.terraform.io/downloads.html) installed on your local machine.
- An active Microsoft Azure account.
- SSH access to the virtual machine.

## Terraform Setup

1. Clone or download the repository containing the Terraform configuration files.

2. Navigate to the directory containing the Terraform configuration files.

3. Initialize Terraform by running the following command:

   ```bash
   terraform init
   ```

4. Review and customize the `variables.tf` file to set your Azure credentials and other configuration parameters.

5. Deploy the virtual machine by running the following command:

   ```bash
   terraform apply
   ```

   Follow the prompts and confirm the deployment. Terraform will create the virtual machine based on the specified configuration.

6. Once the deployment is complete, note down the public IP address of the virtual machine.

---
