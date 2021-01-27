#### Dependencies ####
# - Resource Group
# - network.tf
# - data.tf

resource "azurerm_network_security_group" "datasci_nodes_nsg" {
  name                = join("-", ["nsg", var.cluster_name, var.environment])
  resource_group_name = var.resource_group_name
  location            = var.location

  tags = var.default_tags
}

resource "azurerm_network_security_rule" "datasci_nodes_rules_notebook" {
  name                        = "NOTEB"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "9999"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.datasci_nodes_nsg.name
}

resource "azurerm_network_security_rule" "datasci_nodes_rules_local" {
  count                       = var.source_from_vault ? 0 : 1
  name                        = "SSH"
  priority                    = 1001
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = chomp(data.http.myip.0.body)
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.datasci_nodes_nsg.name
}
resource "azurerm_network_security_rule" "datasci_nodes_rules_with_vault" {
  count                       = var.source_from_vault ? length(local.remote_ips) : 0
  name                        = "SSH-${count.index}"
  priority                    = "20${count.index}"
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = local.remote_ips[count.index]
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.datasci_nodes_nsg.name
}

resource "azurerm_subnet_network_security_group_association" "subnet_nsg" {
  subnet_id                 = azurerm_subnet.subnet_data.id
  network_security_group_id = azurerm_network_security_group.datasci_nodes_nsg.id
}

output "security_group_datasci_nodes_nsg" {
  value = azurerm_network_security_group.datasci_nodes_nsg
}