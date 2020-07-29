create_clock -period "20.000 ns" -name sys_clk  [get_ports {sys_clk}]

derive_pll_clocks
derive_clock_uncertainty

# HPS peripherals port false path setting to workaround the unconstraint path (setting false_path for hps_0 ports will not affect the routing as it is hard silicon)

set_false_path -from * -to [get_ports {usb1_clk}]
set_false_path -from * -to [get_ports {eth1_tx_clk}] 
set_false_path -from * -to [get_ports {eth1_tx_d[0]}] 
set_false_path -from * -to [get_ports {eth1_tx_d[1]}] 
set_false_path -from * -to [get_ports {eth1_tx_d[2]}] 
set_false_path -from * -to [get_ports {eth1_tx_d[3]}] 
set_false_path -from * -to [get_ports {eth1_mdc}] 
set_false_path -from * -to [get_ports {eth1_tx_ctl}] 
set_false_path -from * -to [get_ports {qspi_ss0}] 
set_false_path -from * -to [get_ports {qspi_clk}] 
set_false_path -from * -to [get_ports {sdio_clk}] 
set_false_path -from * -to [get_ports {usb1_stp}] 
set_false_path -from * -to [get_ports {uart0_tx}] 
set_false_path -from * -to [get_ports {uart0_rx}]

set_false_path -from * -to [get_ports {eth1_mdio}] 
set_false_path -from * -to [get_ports {qspi_io[0]}] 
set_false_path -from * -to [get_ports {qspi_io[1]}] 
set_false_path -from * -to [get_ports {qspi_io[2]}] 
set_false_path -from * -to [get_ports {qspi_io[3]}] 
set_false_path -from * -to [get_ports {sdio_cmd}] 
set_false_path -from * -to [get_ports {sdio_d[0]}] 
set_false_path -from * -to [get_ports {sdio_d[1]}] 
set_false_path -from * -to [get_ports {sdio_d[2]}] 
set_false_path -from * -to [get_ports {sdio_d[3]}] 
set_false_path -from * -to [get_ports {usb1_d[0]}] 
set_false_path -from * -to [get_ports {usb1_d[1]}] 
set_false_path -from * -to [get_ports {usb1_d[2]}] 
set_false_path -from * -to [get_ports {usb1_d[3]}] 
set_false_path -from * -to [get_ports {usb1_d[4]}] 
set_false_path -from * -to [get_ports {usb1_d[5]}] 
set_false_path -from * -to [get_ports {usb1_d[6]}] 
set_false_path -from * -to [get_ports {usb1_d[7]}] 
set_false_path -from * -to [get_ports {hps_sda}] 
set_false_path -from * -to [get_ports {hps_scl}]

# removed temporarily for prototype hardware, resinsert for alpha hardware
#set_false_path -from * -to [get_ports {fmc_sda}] 
#set_false_path -from * -to [get_ports {fmc_scl}]

# added temporarily for prototype hardware, remove for alpha hardware
set_false_path -from * -to [get_ports {hdmi_i2c_sda}] 
set_false_path -from * -to [get_ports {hdmi_i2c_scl}]

set_false_path -from * -to [get_ports {link_st}] 
set_false_path -from * -to [get_ports {rx_er}] 
set_false_path -from * -to [get_ports {phy_int}] 
set_false_path -from * -to [get_ports {eth_rst}] 
set_false_path -from * -to [get_ports {phy_led1}] 
set_false_path -from * -to [get_ports {fmc_pg_c2m}] 
set_false_path -from * -to [get_ports {fmc_prsnt_m2c}] 
set_false_path -from * -to [get_ports {usb_rst}] 
set_false_path -from * -to [get_ports {cpu_gpio_0}] 
set_false_path -from * -to [get_ports {cpu_gpio_1}]
set_false_path -from * -to [get_ports {led_hps_1}] 
set_false_path -from * -to [get_ports {led_hps_2}]
set_false_path -from * -to [get_ports {therm_n}]
set_false_path -from * -to [get_ports {alert_n}]
set_false_path -from * -to [get_ports {user_btn_hps}]
set_false_path -from * -to [get_ports {status}]
set_false_path -from * -to [get_ports {as_rst}]
set_false_path -from * -to [get_ports {qspi_rst}]

set_false_path -from [get_ports {eth1_mdio}] -to *
set_false_path -from [get_ports {qspi_io[0]}] -to *
set_false_path -from [get_ports {qspi_io[1]}] -to *
set_false_path -from [get_ports {qspi_io[2]}] -to *
set_false_path -from [get_ports {qspi_io[3]}] -to *
set_false_path -from [get_ports {sdio_cmd}] -to *
set_false_path -from [get_ports {sdio_d[0]}] -to *
set_false_path -from [get_ports {sdio_d[1]}] -to *
set_false_path -from [get_ports {sdio_d[2]}] -to *
set_false_path -from [get_ports {sdio_d[3]}] -to *
set_false_path -from [get_ports {usb1_d[0]}] -to *
set_false_path -from [get_ports {usb1_d[1]}] -to *
set_false_path -from [get_ports {usb1_d[2]}] -to *
set_false_path -from [get_ports {usb1_d[3]}] -to *
set_false_path -from [get_ports {usb1_d[4]}] -to *
set_false_path -from [get_ports {usb1_d[5]}] -to *
set_false_path -from [get_ports {usb1_d[6]}] -to *
set_false_path -from [get_ports {usb1_d[7]}] -to *
set_false_path -from [get_ports {hps_scl}] -to *
set_false_path -from [get_ports {hps_sda}] -to *

# removed temporarily for prototype hardware, resinsert for alpha hardware
#set_false_path -from [get_ports {fmc_scl}] -to *
#set_false_path -from [get_ports {fmc_sda}] -to *

# added temporarily for prototype hardware, remove for alpha hardware
#set_false_path -from [get_ports {hdmi_i2c_scl}] -to *
#set_false_path -from [get_ports {hdmi_i2c_sda}] -to *

set_false_path -from [get_ports {link_st}] -to *
set_false_path -from [get_ports {rx_er}] -to *
set_false_path -from [get_ports {phy_int}] -to *
set_false_path -from [get_ports {eth_rst}] -to *
set_false_path -from [get_ports {phy_led1}] -to *
set_false_path -from [get_ports {fmc_pg_c2m}] -to *
set_false_path -from [get_ports {fmc_prsnt_m2c}] -to *
set_false_path -from [get_ports {usb_rst}] -to *
set_false_path -from [get_ports {cpu_gpio_0}] -to *
set_false_path -from [get_ports {cpu_gpio_1}] -to *
set_false_path -from [get_ports {led_hps_1}] -to *
set_false_path -from [get_ports {led_hps_2}] -to *
set_false_path -from [get_ports {therm_n}] -to *
set_false_path -from [get_ports {alert_n}] -to *
set_false_path -from [get_ports {user_btn_hps}] -to *
set_false_path -from [get_ports {status}] -to *
set_false_path -from [get_ports {as_rst}] -to *
set_false_path -from [get_ports {qspi_rst}] -to *

set_false_path -from [get_ports {eth1_rx_ctl}] -to *
set_false_path -from [get_ports {eth1_rx_clk}] -to *
set_false_path -from [get_ports {eth1_rx_d[0]}] -to *
set_false_path -from [get_ports {eth1_rx_d[1]}] -to *
set_false_path -from [get_ports {eth1_rx_d[2]}] -to *
set_false_path -from [get_ports {eth1_rx_d[3]}] -to *
set_false_path -from [get_ports {usb1_clk}] -to *
set_false_path -from [get_ports {usb1_dir}] -to *
set_false_path -from [get_ports {usb1_nxt}] -to *
set_false_path -from [get_ports {uart0_tx}] -to *
set_false_path -from [get_ports {uart0_rx}] -to *

# frame reader seems to use the wrong reset!

set_false_path -from [get_registers *altera_reset_synchronizer:alt_rst_sync_uq1|altera_reset_synchronizer_int_chain_out*]
