resource "azurerm_bastion_host" "bastion" {
  name                = "bastion-host"
  location            = var.location
  resource_group_name = var.resource_group_name
  public_ip_address_id = azurerm_public_ip.vm_public_ip.id
}