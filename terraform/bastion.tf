# resource "azurerm_bastion_host" "bastion" {
#   name                = "fsm-bastion"
#   location            = var.location
#   resource_group_name = var.resource_group_name

#   ip_configuration {
#     name                 = "bastion-ip-config"
#     subnet_id            = azurerm_subnet.subnet.id
#     public_ip_address_id = azurerm_public_ip.vm_public_ip.id  
#   }
# }
